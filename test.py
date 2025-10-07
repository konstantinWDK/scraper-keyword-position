#!/usr/bin/env python3
"""
Script de prueba rápida para el scraper
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("🔍 Probando importaciones...")
    
    try:
        from config.settings import Config, config
        print("✅ Config importado correctamente")
        
        from stealth_scraper import StealthSerpScraper  
        print("✅ StealthSerpScraper importado correctamente")
        
        from utils import KeywordManager, ResultsAnalyzer
        print("✅ Utils importados correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_config():
    """Prueba la configuración"""
    print("\n🔧 Probando configuración...")
    
    try:
        from config.settings import Config
        
        Config.print_config()
        
        # Validar configuración
        from utils import ConfigValidator
        issues = ConfigValidator.validate_config(Config.to_dict())
        
        if issues:
            print("\n⚠️  Problemas encontrados:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("✅ Configuración válida")
            
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_google_suggest():
    """Prueba Google Suggest sin proxies"""
    print("\n🔍 Probando Google Suggest...")
    
    try:
        from config.settings import config
        from stealth_scraper import StealthSerpScraper
        
        # Configuración de prueba sin proxies
        test_config = config.copy()
        test_config['PROXIES'] = []  # Sin proxies para prueba rápida
        
        scraper = StealthSerpScraper(test_config)
        
        # Probar con keyword simple
        suggestions = scraper.google_suggest_scraper("python", country="US", language="en")
        
        if suggestions:
            print(f"✅ Google Suggest funcionando - {len(suggestions)} sugerencias:")
            for i, suggestion in enumerate(suggestions[:5], 1):
                print(f"   {i}. {suggestion}")
            if len(suggestions) > 5:
                print(f"   ... y {len(suggestions) - 5} más")
            return True
        else:
            print("❌ No se obtuvieron sugerencias")
            return False
            
    except Exception as e:
        print(f"❌ Error en Google Suggest: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SCRAPER")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config), 
        ("Google Suggest", test_google_suggest)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
    
    print("\n" + "="*50)
    print(f"📊 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El scraper está listo.")
        print("\n📖 Próximos pasos:")
        print("   1. Configura proxies en config/.env (recomendado)")
        print("   2. Ejecuta: python src/main.py --test")
        print("   3. Prueba con tus keywords: python src/main.py --keywords 'tu keyword' --domain tu-dominio.com")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        print("💡 Tip: Asegúrate de haber instalado todas las dependencias con ./install.sh")

if __name__ == "__main__":
    main()