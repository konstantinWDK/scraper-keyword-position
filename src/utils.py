"""
Utilidades para el scraper de keywords y posiciones
"""

import os
import json
import pandas as pd
from pathlib import Path
import time
from urllib.parse import urlparse
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

class KeywordManager:
    """Gestor de keywords"""
    
    @staticmethod
    def load_keywords(file_path):
        """Carga keywords desde archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f.readlines() if line.strip()]
            print(f"✅ Cargadas {len(keywords)} keywords desde {file_path}")
            return keywords
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error cargando keywords: {e}")
            return []
    
    @staticmethod
    def save_keywords(keywords, filename):
        """Guarda keywords en archivo"""
        try:
            # Crear directorio data si no existe
            os.makedirs('data', exist_ok=True)
            
            file_path = f"data/{filename}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                for keyword in keywords:
                    f.write(f"{keyword}\n")
            
            print(f"✅ Keywords guardadas en {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ Error guardando keywords: {e}")
            return None
    
    @staticmethod
    def deduplicate_keywords(keywords):
        """Elimina keywords duplicadas manteniendo orden"""
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            keyword_lower = keyword.lower().strip()
            if keyword_lower not in seen:
                seen.add(keyword_lower)
                unique_keywords.append(keyword)
        return unique_keywords
    
    @staticmethod
    def filter_keywords(keywords, min_length=3, max_length=100, exclude_words=None):
        """Filtra keywords por criterios"""
        if exclude_words is None:
            exclude_words = ['xxx', 'porn', 'sex']  # Palabras a excluir
        
        filtered = []
        for keyword in keywords:
            # Filtrar por longitud
            if not (min_length <= len(keyword) <= max_length):
                continue
            
            # Filtrar palabras excluidas
            if any(word.lower() in keyword.lower() for word in exclude_words):
                continue
            
            filtered.append(keyword)
        
        return filtered

class ResultsAnalyzer:
    """Analizador de resultados"""
    
    def __init__(self):
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def load_results(self, file_path):
        """Carga resultados desde archivo CSV o JSON"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
            else:
                print(f"❌ Formato de archivo no soportado: {file_path}")
                return None
        except Exception as e:
            print(f"❌ Error cargando resultados: {e}")
            return None
    
    def analyze_file(self, file_path):
        """Analiza un archivo específico"""
        df = self.load_results(file_path)
        if df is not None:
            self.print_analysis(df)
    
    def analyze_latest(self):
        """Analiza el archivo más reciente"""
        csv_files = list(self.data_dir.glob('*.csv'))
        if not csv_files:
            print("❌ No se encontraron archivos CSV para analizar")
            return
        
        latest_file = max(csv_files, key=os.path.getctime)
        print(f"📊 Analizando archivo más reciente: {latest_file}")
        self.analyze_file(latest_file)
    
    def print_analysis(self, df):
        """Imprime análisis detallado"""
        print("\n" + "="*60)
        print("📊 ANÁLISIS DE RESULTADOS")
        print("="*60)
        
        # Estadísticas generales
        print(f"📋 Total de registros: {len(df)}")
        print(f"🔑 Keywords únicas: {df['keyword'].nunique()}")
        print(f"🌐 Dominios únicos: {df['domain'].nunique()}")
        
        if 'page' in df.columns:
            print(f"📄 Páginas scrapeadas: {df['page'].max()}")
        
        # Análisis de posiciones
        print(f"\n📈 ANÁLISIS DE POSICIONES:")
        print(f"   Posición promedio: {df['position'].mean():.2f}")
        print(f"   Posición mediana: {df['position'].median():.2f}")
        print(f"   Mejor posición: {df['position'].min()}")
        print(f"   Peor posición: {df['position'].max()}")
        
        # Top 10 posiciones
        top_10 = df[df['position'] <= 10]
        print(f"   Resultados en TOP 10: {len(top_10)} ({len(top_10)/len(df)*100:.1f}%)")
        
        # Top 3 posiciones
        top_3 = df[df['position'] <= 3]
        print(f"   Resultados en TOP 3: {len(top_3)} ({len(top_3)/len(df)*100:.1f}%)")
        
        # Análisis por dominio
        print(f"\n🌐 TOP 10 DOMINIOS:")
        domain_counts = df['domain'].value_counts().head(10)
        for i, (domain, count) in enumerate(domain_counts.items(), 1):
            avg_pos = df[df['domain'] == domain]['position'].mean()
            print(f"   {i:2d}. {domain:<30} - {count:3d} resultados (pos. prom: {avg_pos:.1f})")
        
        # Keywords con mejores posiciones
        print(f"\n🏆 TOP 10 KEYWORDS (mejor posición):")
        best_keywords = df.loc[df.groupby('keyword')['position'].idxmin()].sort_values('position').head(10)
        for i, row in best_keywords.iterrows():
            print(f"   {row['position']:2d}. {row['keyword']:<40} - {row['domain']}")
        
        # Distribución de posiciones
        print(f"\n📊 DISTRIBUCIÓN DE POSICIONES:")
        position_ranges = [
            (1, 3, "TOP 3"),
            (4, 10, "TOP 10"),
            (11, 20, "Página 2"),
            (21, 50, "Páginas 3-5"),
            (51, 100, "Páginas 6-10")
        ]
        
        for min_pos, max_pos, label in position_ranges:
            count = len(df[(df['position'] >= min_pos) & (df['position'] <= max_pos)])
            percentage = count / len(df) * 100
            print(f"   {label:<12}: {count:4d} ({percentage:5.1f}%)")
    
    def export_summary(self, df, output_file):
        """Exporta resumen a archivo"""
        try:
            summary = {
                'total_records': len(df),
                'unique_keywords': df['keyword'].nunique(),
                'unique_domains': df['domain'].nunique(),
                'avg_position': df['position'].mean(),
                'median_position': df['position'].median(),
                'top_10_count': len(df[df['position'] <= 10]),
                'top_3_count': len(df[df['position'] <= 3]),
                'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Resumen exportado a {output_file}")
        except Exception as e:
            print(f"❌ Error exportando resumen: {e}")

class ProxyTester:
    """Tester de proxies"""
    
    @staticmethod
    def test_proxy(proxy_string, timeout=10):
        """Prueba un proxy"""
        import requests
        
        try:
            proxy_dict = {
                'http': f'http://{proxy_string}',
                'https': f'http://{proxy_string}'
            }
            
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxy_dict,
                timeout=timeout
            )
            
            if response.status_code == 200:
                ip_info = response.json()
                return True, ip_info.get('origin', 'Unknown')
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def test_proxy_list(proxy_list):
        """Prueba lista de proxies"""
        print("🔍 Probando proxies...")
        
        working_proxies = []
        for i, proxy in enumerate(proxy_list, 1):
            print(f"   {i}/{len(proxy_list)} - {proxy:<30}", end=" ")
            
            is_working, result = ProxyTester.test_proxy(proxy)
            
            if is_working:
                print(f"✅ OK - IP: {result}")
                working_proxies.append(proxy)
            else:
                print(f"❌ Error: {result}")
        
        print(f"\n📊 Resultado: {len(working_proxies)}/{len(proxy_list)} proxies funcionando")
        return working_proxies

class ConfigValidator:
    """Validador de configuración"""
    
    @staticmethod
    def validate_config(config):
        """Valida la configuración"""
        issues = []
        
        # Validar proxies
        if not config.get('PROXIES'):
            issues.append("⚠️  No hay proxies configurados - Alto riesgo de bloqueo")
        elif len(config['PROXIES']) < 3:
            issues.append("⚠️  Pocos proxies configurados - Recomendado mínimo 3")
        
        # Validar delays
        if config.get('MIN_KEYWORD_DELAY', 0) < 3:
            issues.append("⚠️  Delay mínimo muy bajo - Riesgo de detección")
        
        # Validar configuración
        if config.get('PAGES_TO_SCRAPE', 1) > 5:
            issues.append("⚠️  Muchas páginas - Puede ser lento y detectado")
        
        return issues
    
    @staticmethod
    def print_validation(config):
        """Imprime validación de configuración"""
        issues = ConfigValidator.validate_config(config)
        
        if not issues:
            print("✅ Configuración válida")
        else:
            print("⚠️  Problemas de configuración encontrados:")
            for issue in issues:
                print(f"   {issue}")
        
        return len(issues) == 0