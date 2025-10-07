#!/usr/bin/env python3
"""
Scraper de Keywords y Posiciones - Anti-detección 2025
Uso: python main.py [opciones]
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Añadir directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, config
from stealth_scraper import StealthSerpScraper
from utils import KeywordManager, ResultsAnalyzer
from colorama import Fore, Style, init

# Inicializar colorama para colores en terminal
init(autoreset=True)

def print_banner():
    """Imprime banner del scraper"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    KEYWORD POSITION SCRAPER                 ║
║                     Anti-detección 2025                     ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def main():
    parser = argparse.ArgumentParser(
        description='Scraper de posiciones de keywords con anti-detección',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --keywords "seo,marketing digital" --domain example.com
  python main.py --keyword-file keywords.txt --domain example.com --pages 3
  python main.py --suggest "marketing" --country ES --language es
  python main.py --batch keywords.txt --domain example.com --output results_custom
        """
    )
    
    # Argumentos principales
    parser.add_argument('--keywords', '-k', 
                       help='Keywords separadas por comas')
    parser.add_argument('--keyword-file', '-f', 
                       help='Archivo con keywords (una por línea)')
    parser.add_argument('--domain', '-d', 
                       help='Dominio a buscar en los resultados')
    parser.add_argument('--pages', '-p', type=int, default=1,
                       help='Número de páginas a scrapear (default: 1)')
    
    # Funciones especiales
    parser.add_argument('--suggest', '-s', 
                       help='Generar keywords con Google Suggest')
    parser.add_argument('--batch', '-b', 
                       help='Procesamiento por lotes desde archivo')
    
    # Configuración
    parser.add_argument('--country', default='US',
                       help='País para la búsqueda (default: US)')
    parser.add_argument('--language', default='en',
                       help='Idioma para la búsqueda (default: en)')
    parser.add_argument('--output', '-o',
                       help='Nombre del archivo de salida (sin extensión)')
    
    # Opciones de análisis
    parser.add_argument('--analyze', '-a', action='store_true',
                       help='Analizar resultados existentes')
    parser.add_argument('--analyze-file', 
                       help='Archivo específico para analizar')
    
    # Modo de prueba
    parser.add_argument('--test', action='store_true',
                       help='Modo de prueba con una keyword')
    parser.add_argument('--config', action='store_true',
                       help='Mostrar configuración actual')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Mostrar configuración si se solicita
    if args.config:
        Config.print_config()
        return
    

    # Analizar resultados existentes
    if args.analyze:
        analyzer = ResultsAnalyzer()
        if args.analyze_file:
            analyzer.analyze_file(args.analyze_file)
        else:
            analyzer.analyze_latest()
        return
    
    # Validar argumentos
    if not any([args.keywords, args.keyword_file, args.suggest, args.batch, args.test]):
        print(f"{Fore.RED}❌ Error: Debes especificar keywords, archivo, suggest o batch{Style.RESET_ALL}")
        parser.print_help()
        return
    
    # Inicializar scraper
    print(f"{Fore.YELLOW}🔧 Inicializando scraper...{Style.RESET_ALL}")
    scraper = StealthSerpScraper(config)
    keyword_manager = KeywordManager()
    
    try:
        # Modo de prueba
        if args.test:
            print(f"{Fore.BLUE}🧪 Modo de prueba - Testing con keyword: 'python scraping'{Style.RESET_ALL}")
            test_keywords = ['python scraping']
            results = scraper.batch_position_check(test_keywords, args.domain or 'github.com', 1)
            
            if results:
                scraper.save_results(results, 'test_results')
                print(f"{Fore.GREEN}✅ Prueba completada. Revisa los archivos en data/{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ No se obtuvieron resultados en la prueba{Style.RESET_ALL}")
            return
        
        # Google Suggest
        if args.suggest:
            print(f"{Fore.BLUE}🔍 Generando keywords con Google Suggest para: '{args.suggest}'{Style.RESET_ALL}")
            suggestions = scraper.google_suggest_scraper(
                args.suggest, 
                country=args.country, 
                language=args.language
            )
            
            if suggestions:
                print(f"{Fore.GREEN}✅ Encontradas {len(suggestions)} sugerencias:{Style.RESET_ALL}")
                for i, suggestion in enumerate(suggestions[:10], 1):
                    print(f"   {i}. {suggestion}")
                
                # Guardar sugerencias
                keyword_manager.save_keywords(suggestions, f'suggestions_{args.suggest}')
                
                # Preguntar si continuar con scraping
                if args.domain:
                    response = input(f"\n{Fore.CYAN}¿Continuar con scraping de posiciones? (y/n): {Style.RESET_ALL}")
                    if response.lower() == 'y':
                        keywords = suggestions
                    else:
                        return
                else:
                    print(f"{Fore.YELLOW}💡 Usa --domain para buscar posiciones de estas keywords{Style.RESET_ALL}")
                    return
            else:
                print(f"{Fore.RED}❌ No se encontraron sugerencias{Style.RESET_ALL}")
                return
        
        # Cargar keywords
        elif args.keywords:
            keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
        elif args.keyword_file or args.batch:
            file_path = args.keyword_file or args.batch
            keywords = keyword_manager.load_keywords(file_path)
        
        if not keywords:
            print(f"{Fore.RED}❌ No se cargaron keywords{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}📋 Keywords cargadas: {len(keywords)}{Style.RESET_ALL}")
        for i, kw in enumerate(keywords[:5], 1):
            print(f"   {i}. {kw}")
        if len(keywords) > 5:
            print(f"   ... y {len(keywords) - 5} más")
        
        # Verificar dominio
        if not args.domain:
            print(f"{Fore.YELLOW}⚠️  No se especificó dominio. Se mostrarán todas las posiciones.{Style.RESET_ALL}")
        
        # Confirmar antes de empezar
        estimated_time = len(keywords) * (config['MIN_KEYWORD_DELAY'] + config['MAX_KEYWORD_DELAY']) / 120
        print(f"{Fore.BLUE}⏱️  Tiempo estimado: {estimated_time:.1f} minutos{Style.RESET_ALL}")
        
        response = input(f"{Fore.CYAN}¿Continuar con el scraping? (y/n): {Style.RESET_ALL}")
        if response.lower() != 'y':
            print(f"{Fore.YELLOW}❌ Cancelado por el usuario{Style.RESET_ALL}")
            return
        
        # Ejecutar scraping
        print(f"{Fore.GREEN}🚀 Iniciando scraping...{Style.RESET_ALL}")
        results = scraper.batch_position_check(keywords, args.domain, args.pages)
        
        if results:
            # Guardar resultados
            output_name = args.output or f'positions_{args.domain}' if args.domain else 'positions_all'
            scraper.save_results(results, output_name)
            
            # Mostrar estadísticas rápidas
            total_positions = len(results)
            unique_keywords = len(set([r['keyword'] for r in results]))
            
            if args.domain:
                domain_results = [r for r in results if args.domain.lower() in r['domain'].lower()]
                print(f"{Fore.GREEN}📊 Resumen:{Style.RESET_ALL}")
                print(f"   Keywords procesadas: {unique_keywords}")
                print(f"   Posiciones de {args.domain}: {len(domain_results)}")
                print(f"   Total posiciones encontradas: {total_positions}")
                
                if domain_results:
                    avg_position = sum([r['position'] for r in domain_results]) / len(domain_results)
                    print(f"   Posición promedio: {avg_position:.1f}")
            else:
                print(f"{Fore.GREEN}📊 Resumen:{Style.RESET_ALL}")
                print(f"   Keywords procesadas: {unique_keywords}")
                print(f"   Total posiciones encontradas: {total_positions}")
            
            print(f"{Fore.GREEN}✅ Scraping completado. Revisa los archivos en data/{Style.RESET_ALL}")
            
        else:
            print(f"{Fore.RED}❌ No se obtuvieron resultados{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}❌ Cancelado por el usuario{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
