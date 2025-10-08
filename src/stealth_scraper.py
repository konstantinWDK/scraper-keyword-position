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

    def single_keyword_position_check(self, keyword, target_domain=None, pages=1):
        """Analiza una sola keyword y devuelve todos los resultados encontrados"""
        return self.serp_scraper_api(keyword, target_domain, pages)

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

    def google_suggest_scraper(self, keyword, country="US", language="en"):
        """Obtiene sugerencias de Google Suggest para una keyword"""
        suggestions = []

        try:
            # Google Suggest API URL
            url = "https://www.google.com/complete/search"

            params = {
                'q': keyword,
                'client': 'firefox',
                'hl': language.lower(),
                'gl': country.lower()
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Language': f'{language.lower()}-{country.lower()},{language.lower()};q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }

            response = self.session.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 200:
                # Google Suggest devuelve JSONP, pero podemos parsear como JSON
                try:
                    # Cuando no hay callback, devuelve JSON directo
                    data = response.json()

                    # El formato típico de Google Suggest es:
                    # [query, [suggestion1, suggestion2, ...], ...]
                    if isinstance(data, list) and len(data) >= 2:
                        suggestions_list = data[1] if isinstance(data[1], list) else []

                        # Filtrar solo strings válidos
                        for suggestion in suggestions_list:
                            if isinstance(suggestion, str) and suggestion.strip():
                                suggestions.append(suggestion.strip())

                    elif isinstance(data, list) and len(data) > 0:
                        # A veces solo devuelve la lista de sugerencias
                        for item in data:
                            if isinstance(item, str) and item.strip():
                                suggestions.append(item.strip())

                except json.JSONDecodeError:
                    # Si no es JSON directo, puede ser JSONP
                    text = response.text.strip()
                    if text.startswith('(') and text.endswith(')'):
                        # Intentar quitar el callback function()
                        try:
                            json_text = text[1:-1]  # Quitar paréntesis
                            data = json.loads(json_text)
                            if isinstance(data, list) and len(data) >= 2:
                                suggestions_list = data[1] if isinstance(data[1], list) else []
                                for suggestion in suggestions_list:
                                    if isinstance(suggestion, str) and suggestion.strip():
                                        suggestions.append(suggestion.strip())
                        except json.JSONDecodeError:
                            pass

                # Limitar a 10 sugerencias máxima
                suggestions = suggestions[:10]

                # Log detallado solo si hay sugerencias y para depuración
                if suggestions:
                    self.logger.debug(f"Encontradas {len(suggestions)} sugerencias para '{keyword}': {suggestions[:3]}...")
                else:
                    self.logger.debug(f"No se encontraron sugerencias adicionales para '{keyword}'")

        except Exception as e:
            self.logger.warning(f"Error obteniendo sugerencias para '{keyword}': {str(e)}")

        return suggestions
