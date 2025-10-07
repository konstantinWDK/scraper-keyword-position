#!/usr/bin/env python3
"""
Script para probar proxies gratuitos
Verifica qué proxies de la lista están funcionando
"""

import sys
import os
from pathlib import Path

# Añadir directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import ProxyTester

def load_proxies_from_file(file_path="proxies_formatted.txt"):
    """Carga proxies desde archivo convertido"""
    proxies = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorar líneas vacías
                if line and ':' in line:
                    proxies.append(line)
        return proxies
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}")
        print(f"💡 Ejecuta primero: python3 convert_proxies.py")
        return []

def test_proxies():
    """Prueba todos los proxies del archivo"""
    print("🔍 Probando proxies gratuitos...")
    print("=" * 50)
    
    # Cargar proxies desde archivo
    proxies = load_proxies_from_file()
    
    if not proxies:
        print("❌ No se encontraron proxies para probar")
        return
    
    print(f"📋 Encontrados {len(proxies)} proxies para probar")
    print()
    
    # Probar proxies
    working_proxies = ProxyTester.test_proxy_list(proxies)
    
    print()
    print("=" * 50)
    print("📊 RESUMEN FINAL")
    print(f"✅ Proxies funcionando: {len(working_proxies)}/{len(proxies)}")
    
    if working_proxies:
        print("\n🎯 PROXIES RECOMENDADOS (funcionando):")
        for i, proxy in enumerate(working_proxies[:10], 1):  # Mostrar solo los primeros 10
            print(f"   {i}. {proxy}")
        
        if len(working_proxies) > 10:
            print(f"   ... y {len(working_proxies) - 10} más")
        
        # Guardar proxies funcionando en archivo
        output_file = "proxies_funcionando.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Proxies gratuitos funcionando - Actualizado automáticamente\n")
            for proxy in working_proxies:
                f.write(f"{proxy}\n")
        
        print(f"\n💾 Lista de proxies funcionando guardada en: {output_file}")
        
        # Mostrar configuración de ejemplo
        print("\n⚙️  CONFIGURACIÓN EJEMPLO para config/.env:")
        for i, proxy in enumerate(working_proxies[:5], 1):
            print(f"PROXY_{i}={proxy}")
    
    else:
        print("❌ No se encontraron proxies funcionando")
        print("💡 Intenta actualizar la lista de proxies o usar proxies premium")

def quick_test():
    """Prueba rápida de algunos proxies"""
    print("🚀 Prueba rápida de proxies...")
    
    # Proxies de alta velocidad para probar primero
    test_proxies = [
        "51.158.68.68:8811",
        "188.166.59.17:8888", 
        "185.162.251.147:80",
        "45.77.56.1:3128",
        "103.152.112.145:8080"
    ]
    
    working = ProxyTester.test_proxy_list(test_proxies)
    
    if working:
        print(f"✅ {len(working)}/{len(test_proxies)} proxies funcionando")
        return working
    else:
        print("❌ Ningún proxy funcionó en la prueba rápida")
        return []

if __name__ == "__main__":
    print("🔄 Keyword Position Scraper - Probador de Proxies")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        test_proxies()
