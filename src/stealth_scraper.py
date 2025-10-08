import random
import time
import json
import logging
import requests
from urllib.parse import quote_plus, urlparse
import pandas as pd
from tqdm import tqdm
import os

class StealthSerpScraper:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.results = []

        # Crear directorios necesarios
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        logs_dir = os.path.join(parent_dir, 'logs')
        data_dir = os.path.join(parent_dir, 'data')

        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)

        # Configurar logging con path absoluto
        log_file_path = os.path.join(logs_dir, 'scraper.log')
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S',
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_google_api_headers(self):
        """Headers para llamadas a Google API"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }

    def serp_scraper_api(self, keyword, target_domain=None, pages=1):
        """Scraper de posiciones usando SOLAMENTE Google Custom Search API"""
        results = []

        api_key = self.config.get('GOOGLE_API_KEY', '')
        search_engine_id = self.config.get('GOOGLE_SEARCH_ENGINE_ID', '')

        if not api_key or not search_engine_id:
            self.logger.error("Google API Key o Search Engine ID no configurados")
            return results

        self.logger.info(f"🔍 Consultando Google API para keyword: '{keyword}'")

        try:
            # Google API permite máximo 10 resultados por petición (num=10)
            # Para múltiples páginas, necesitamos múltiples llamadas
            max_results_per_page = 10
            total_desired_results = pages * 10

            start_index = 1  # Google API inicia desde 1

            while start_index <= total_desired_results and start_index <= 91:  # Máximo 91 para Google
                # Preparar parámetros para Google Custom Search API
                params = {
                    'key': api_key,
                    'cx': search_engine_id,
                    'q': keyword,
                    'num': min(10, total_desired_results - start_index + 1),
                    'start': start_index,
                    'gl': self.config.get('DEFAULT_COUNTRY', 'US').lower(),  # País
                    'hl': self.config.get('DEFAULT_LANGUAGE', 'en').lower()  # Idioma
                }

                # Hacer la petición
                headers = self.get_google_api_headers()
                response = self.session.get(
                    'https://www.googleapis.com/customsearch/v1',
                    params=params,
                    headers=headers,
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()

                    if 'items' in data:
                        items = data['items']

                        for i, item in enumerate(items):
                            position = start_index + i - 1  # Posición real
                            url = item.get('link', '')
                            title = item.get('title', '')
                            snippet = item.get('snippet', '')

                            domain = urlparse(url).netloc.lower()

                            result = {
                                'keyword': keyword,
                                'position': position,
                                'title': title,
                                'url': url,
                                'domain': domain,
                                'snippet': snippet,
                                'page': ((position - 1) // 10) + 1
                            }

                            results.append(result)

                            # Si estamos buscando un dominio específico y lo encontramos
                            if target_domain and target_domain.lower() in domain:
                                self.logger.info(f"🎯 Encontrado {target_domain} en posición {position}")

                        # Preparar para la siguiente página (si hay)
                        start_index += len(items)

                        # Control de rate limiting: delay entre peticiones
                        delay = self.config.get('MIN_KEYWORD_DELAY', 1)
                        time.sleep(delay)
                    else:
                        self.logger.info(f"No encontró más resultados para '{keyword}'")
                        break

                elif response.status_code == 403:
                    data = response.json()
                    error_msg = data.get('error', {}).get('message', '')

                    if "DAILY_LIMIT_EXCEEDED" in error_msg:
                        self.logger.error("🚫 Límite diario de Google API excedido (100 consultas)")
                        break
                    elif "quota" in error_msg.lower():
                        self.logger.error("🚫 Cuota de Google API agotada")
                        break
                    else:
                        self.logger.error(f"🚫 Error de autenticación Google API: {error_msg}")
                        break

                elif response.status_code == 429:
                    self.logger.warning("⏳ Rate limiting de Google API - esperando...")
                    time.sleep(5)  # Esperar y continuar
                    continue

                else:
                    self.logger.error(f"❌ Error HTTP {response.status_code} en API de Google")
                    break

        except Exception as e:
            self.logger.error(f"❌ Error al consultar Google API: {e}")
            return results

        self.logger.info(f"✅ Encontrados {len(results)} resultados para '{keyword}'")
        return results
    
    def batch_position_check(self, keywords, target_domain, pages=1):
        """Verifica posiciones para múltiples keywords usando SOLAMENTE Google API"""
        all_results = []

        self.logger.info(f"🚀 Iniciando verificación de posiciones para {len(keywords)} keywords")

        for i, keyword in enumerate(tqdm(keywords, desc="Verificando posiciones")):
            self.logger.info(f"🔄 Procesando keyword {i+1}/{len(keywords)}: '{keyword}'")

            results = self.serp_scraper_api(keyword, target_domain, pages)
            all_results.extend(results)

            # Delay entre keywords (configurado por usuario)
            if i < len(keywords) - 1:
                delay = random.uniform(
                    self.config.get('MIN_KEYWORD_DELAY', 5),
                    self.config.get('MAX_KEYWORD_DELAY', 15)
                )
                self.logger.info(f"⏳ Esperando {delay:.1f}s antes del siguiente keyword...")
                time.sleep(delay)

        self.logger.info(f"✅ Proceso completado - Total posiciones encontradas: {len(all_results)}")
        return all_results

    def google_suggest_scraper(self, base_keyword, country="US", language="en", max_suggestions=25):
        """Obtiene sugerencias de Google Suggest API para completar keywords"""
        suggestions = []

        try:
            self.logger.info(f"🔍 Obteniendo sugerencias para: '{base_keyword}'")

            # URL de Google Suggest API
            suggest_url = "https://suggestqueries.google.com/complete/search"

            # Variaciones de búsqueda para obtener más sugerencias
            variations = [base_keyword]

            # Añadir variaciones con conectores comunes
            variations.extend([
                f"{base_keyword} o",
                f"{base_keyword} y",
                f"{base_keyword} con",
                f"{base_keyword} para",
                f"{base_keyword} en",
                f"{base_keyword} de",
                f"{base_keyword} como",
                f"{base_keyword} precio",
                f"{base_keyword} más"
            ])

            for variation in variations:
                params = {
                    'client': 'firefox',
                    'q': variation,
                    'hl': language.lower(),
                    'gl': country.upper(),
                    'ds': 'yt'  # También incluya búsquedas de YouTube
                }

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                    'Accept': '*/*',
                    'Accept-Language': f'{language.lower()},{language.lower()};q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                }

                try:
                    response = requests.get(
                        suggest_url,
                        params=params,
                        headers=headers,
                        timeout=self.config.get('REQUEST_TIMEOUT', 10)
                    )

                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if len(data) >= 2 and isinstance(data[1], list):
                                new_suggestions = data[1]
                                suggestions.extend(new_suggestions)
                        except json.JSONDecodeError:
                            self.logger.warning(f"TA respuesta de Google Suggest no es JSON válida para '{variation}'")
                    else:
                        self.logger.warning(f"Sugerencias HTTP {response.status_code} para '{variation}'")

                except requests.RequestException as e:
                    self.logger.warning(f"Error conectando con Google Suggest: {e}")
                    continue

                # Pequeño delay entre búsquedas
                time.sleep(0.5)

            # Limpiar y filtrar sugerencias
            clean_suggestions = []
            base_lower = base_keyword.lower()

            for sug in suggestions:
                if sug and isinstance(sug, str):
                    clean_sug = sug.strip()
                    if (len(clean_sug) > len(base_keyword) + 1 and  # Al menos 2 caracteres adicionales
                        clean_sug.lower() != base_lower and       # No igual a la palabra base
                        not clean_sug.lower().startswith(f"{base_lower} {base_lower}")):  # Evitar duplicados
                        clean_suggestions.append(clean_sug)

            # Eliminar duplicados manteniendo el orden
            seen = set()
            unique_suggestions = []
            for sug in clean_suggestions:
                if sug.lower() not in seen:
                    unique_suggestions.append(sug)
                    seen.add(sug.lower())

            # Limitar cantidad
            final_suggestions = unique_suggestions[:max_suggestions]

            self.logger.info(f"✅ Obtenidas {len(final_suggestions)} sugerencias únicas de Google Suggest")
            return final_suggestions

        except Exception as e:
            self.logger.error(f"❌ Error obteniendo sugerencias: {e}")
            return []

    def keyword_variants_generator(self, keywords, prefix_words=None, suffix_words=None, max_variants_per_keyword=20):
        """Genera variantes long-tail de keywords base"""
        variants = []
        base_keywords = keywords if isinstance(keywords, list) else [keywords]

        # Palabras comunes para prefixes (antes)
        default_prefixes = [
            "mejor", "como", "donde", "precio", "comprar", "tutorial", "guía", "ejemplos",
            "tips", "formulario", "requisitos", "procesos", "sistema", "estándar", "normas",
            "últimas", "nuevo", "actual", "completo", "fácil", "rápido", "sin", "con",
            "para", "por", "gratis", "barato", "profesional", "certificado"
        ]

        # Palabras comunes para suffixes (después)
        default_suffixes = [
            "españa", "madrid", "barcelona", "online", "internet", "web", "app", "móvil",
            "2025", "2024", "actual", "nuevo", "paso a paso", "gratuito", "fácil", "rápido",
            "barato", "profesional", "certificado", "autorizado", "oficial", "sistema",
            "completo", "integral", "total", "incluye", "descuento", "oferta", "promoción"
        ]

        prefix_words = prefix_words or default_prefixes
        suffix_words = suffix_words or default_suffixes

        self.logger.info(f"🔄 Generando variantes para {len(base_keywords)} keywords base")

        for keyword in base_keywords:
            keyword_variants = []

            # Mantener la keyword original
            keyword_variants.append(keyword)

            # Generar variantes con números y cantidades
            if len(keyword.split()) <= 2:  # Solo keywords cortas
                keyword_variants.extend([
                    f"{keyword} 2025",
                    f"mejor {keyword}",
                    f"{keyword} paso a paso",
                    f"como {keyword}",
                    f"donde {keyword}",
                    f"precio {keyword}",
                    f"{keyword} online",
                    f"{keyword} gratuito",
                    f"comprar {keyword}",
                    f"{keyword} barato",
                    f"{keyword} profesional"
                ])

            # Variantes más específicas si la keyword es muy corta
            if len(keyword) < 10 and len(keyword.split()) == 1:
                keyword_variants.extend([
                    f"{keyword} en españa",
                    f"{keyword} madrid",
                    f"{keyword} barcelona",
                    f"cursillo {keyword}",
                    f"curso {keyword}",
                    f"temario {keyword}",
                    f"certificación {keyword}"
                ])

            # Limpiar y añadir las variantes únicas
            clean_variants = []
            seen = set()
            for variant in keyword_variants:
                clean_variant = variant.strip()
                if clean_variant and clean_variant.lower() not in seen and len(clean_variant.split()) <= 4:  # Máximo 4 palabras
                    clean_variants.append(clean_variant)
                    seen.add(clean_variant.lower())

            # Limitar por keyword
            variants.extend(clean_variants[:max_variants_per_keyword])

        # Eliminar duplicados globales
        unique_variants = list(set(variants))

        self.logger.info(f"✅ Generadas {len(unique_variants)} variantes únicas")
        return unique_variants

    def analyze_keyword_competitiveness(self, keyword):
        """Analiza la competitividad de una keyword simulando métricas SEO"""
        # Esta es una implementación simplificada ya que las APIs reales de KW research son pagas
        score = 3.0  # Base neutral

        # Análisis basado en características del keyword
        keyword_length = len(keyword)
        word_count = len(keyword.split())
        has_geo_terms = any(term in keyword.lower() for term in ['españa', 'madrid', 'barcelona', 'español', 'castellano'])
        has_commercial_intent = any(term in keyword.lower() for term in ['comprar', 'precio', 'barato', 'venta', 'oferta', 'promocia'])
        has_long_tail = word_count >= 3

        # Calcular score basado en complejidad y competitividad
        if has_long_tail:
            score -= 1.0  # Long-tail menos competitivo
        if keyword_length < 10:
            score += 1.0  # Keywords cortas más competitivas
        if has_geo_terms:
            score -= 0.5  # Términos geográficos suelen ser menos competitivos
        if has_commercial_intent:
            score += 2.0  # Intent comercial muy competitivo
        if word_count == 1:
            score += 3.0  # Keywords de una palabra muy competitivas

        # Volumen estimado (muy grosero)
        base_volume = 1000
        if keyword_length < 10:
            volume_multiplier = 5.0
        elif keyword_length < 20:
            volume_multiplier = 2.0
        elif keyword_length < 30:
            volume_multiplier = 1.0
        else:
            volume_multiplier = 0.5

        if has_commercial_intent:
            volume_multiplier *= 1.5
        if has_geo_terms:
            volume_multiplier *= 0.7

        estimated_volume = int(base_volume * volume_multiplier)

        # Dificultad basada en score de competencia
        difficulty = min(100, score * 12 + (word_count - 1) * 5)

        # Oportunidad = inverso de dificultad
        opportunity = max(0, 100 - difficulty)
        if has_long_tail:
            opportunity += 10  # Long-tail tiene más oportunidades

        return {
            'keyword': keyword,
            'competition_score': round(score, 1),
            'estimated_volume': estimated_volume,
            'difficulty': round(difficulty, 0),
            'opportunity_score': round(opportunity, 0),
        }

    def save_results(self, results, filename=None):
        """Guarda resultados en CSV y JSON"""
        if not results:
            self.logger.warning("No results to save")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            filename = f"keyword_positions_{timestamp}"
        
        # Guardar como CSV
        df = pd.DataFrame(results)

        # Path absoluto para data (calculado desde src/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_dir_abs = os.path.join(parent_dir, 'data')

        data_file_path = os.path.join(data_dir_abs, f"{filename}.csv")
        df.to_csv(data_file_path, index=False, encoding='utf-8')

        # Guardar como JSON
        json_file_path = os.path.join(data_dir_abs, f"{filename}.json")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Results saved to {data_file_path} and {json_file_path}")
        
        # Estadísticas
        total_keywords = len(set([r['keyword'] for r in results]))
        self.logger.info(f"Total keywords processed: {total_keywords}")
        self.logger.info(f"Total positions found: {len(results)}")
