#!/usr/bin/env python3
"""
Scraper de Keywords y Posiciones - Interfaz Gráfica Principal
Ejecuta la aplicación completa mediante GUI moderna

Uso: python run_gui.py
"""

import sys
import os

def main():
    """Función principal - lanza la interfaz gráfica"""
    try:
        print("🚀 Iniciando Keyword Position Scraper GUI...")

        # Añadir src al path
        src_dir = os.path.join(os.path.dirname(__file__), 'src')
        sys.path.insert(0, src_dir)

        # Verificar que los directorios necesarios existan
        for directory in ['data', 'logs', 'config']:
            os.makedirs(directory, exist_ok=True)

        # Ejecutar la aplicación GUI
        from gui import main as gui_main
        gui_main()

    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando la aplicación: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
