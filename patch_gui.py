#!/usr/bin/env python3
"""
🔧 Script de Parche Automático para GUI
Integra las funcionalidades híbridas en la interfaz gráfica existente
"""

import os
import re
import shutil
from datetime import datetime


def backup_file(filepath):
    """Crea backup del archivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"✅ Backup creado: {backup_path}")
    return backup_path


def patch_gui():
    """Parchea gui.py para integrar funcionalidades híbridas"""
    gui_file = 'src/gui.py'

    if not os.path.exists(gui_file):
        print(f"❌ Error: No se encontró {gui_file}")
        return False

    # Crear backup
    backup_file(gui_file)

    # Leer contenido
    with open(gui_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    # 1. Añadir import de HybridGUIExtensions
    if 'from gui_hybrid_extensions import HybridGUIExtensions' not in content:
        # Buscar la línea de import de ProjectManager
        if 'from project_manager import ProjectManager' in content:
            content = content.replace(
                'from project_manager import ProjectManager',
                'from project_manager import ProjectManager\nfrom gui_hybrid_extensions import HybridGUIExtensions'
            )
            changes_made.append("✅ Import de HybridGUIExtensions añadido")
        else:
            print("⚠️ No se encontró import de ProjectManager, añadiendo al inicio")
            # Añadir después de los imports existentes
            import_section = content.find('from project_manager import')
            if import_section == -1:
                import_section = content.find('import customtkinter')
            if import_section != -1:
                end_of_line = content.find('\n', import_section)
                content = (content[:end_of_line + 1] +
                          'from gui_hybrid_extensions import HybridGUIExtensions\n' +
                          content[end_of_line + 1:])
                changes_made.append("✅ Import de HybridGUIExtensions añadido")

    # 2. Modificar herencia de clase
    class_pattern = r'class KeywordScraperGUI\(ReportMethods\):'
    if re.search(class_pattern, content):
        content = re.sub(
            class_pattern,
            'class KeywordScraperGUI(ReportMethods, HybridGUIExtensions):',
            content
        )
        changes_made.append("✅ Herencia de HybridGUIExtensions añadida a la clase")
    elif 'class KeywordScraperGUI(ReportMethods, HybridGUIExtensions):' in content:
        changes_made.append("ℹ️ La clase ya hereda de HybridGUIExtensions")
    else:
        print("⚠️ No se encontró la declaración de clase KeywordScraperGUI")

    # 3. Añadir llamada a setup_hybrid_tab
    if 'self.setup_hybrid_tab()' not in content:
        # Buscar donde se llama a setup_search_console_tab
        if 'self.setup_search_console_tab()' in content:
            content = content.replace(
                'self.setup_search_console_tab()',
                'self.setup_search_console_tab()\n        self.setup_hybrid_tab()  # Pestaña híbrida'
            )
            changes_made.append("✅ Llamada a setup_hybrid_tab() añadida")
        else:
            print("⚠️ No se encontró setup_search_console_tab(), busca setup_gui manualmente")
    else:
        changes_made.append("ℹ️ Ya existe llamada a setup_hybrid_tab()")

    # Verificar si se hicieron cambios
    if content == original_content:
        print("\nℹ️ No se realizaron cambios. La GUI ya parece estar parcheada.")
        return True

    # Guardar archivo parcheado
    with open(gui_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Mostrar resumen
    print("\n" + "="*60)
    print("✅ GUI PARCHEADA EXITOSAMENTE")
    print("="*60)
    print("\nCambios realizados:")
    for change in changes_made:
        print(f"  {change}")

    print("\n📋 Próximos pasos:")
    print("  1. Verifica que todos los archivos estén en src/:")
    print("     - gui_hybrid_extensions.py")
    print("     - search_console_wrapper.py")
    print("     - sc_scraper_sync.py")
    print("     - hybrid_analyzer.py")
    print("     - hybrid_report_generator.py")
    print("  2. Ejecuta: python run_gui.py")
    print("  3. Busca la nueva pestaña '🔄 Híbrido'")
    print("\n📖 Lee INTEGRACION_GUI.md para más detalles")

    return True


def verify_dependencies():
    """Verifica que todos los archivos necesarios existan"""
    required_files = [
        'src/gui_hybrid_extensions.py',
        'src/search_console_wrapper.py',
        'src/sc_scraper_sync.py',
        'src/hybrid_analyzer.py',
        'src/hybrid_report_generator.py',
        'src/search_console_auth_improved.py'
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print("⚠️ Archivos faltantes:")
        for file in missing:
            print(f"  ❌ {file}")
        print("\nAsegúrate de tener todos los archivos antes de parchear.")
        return False

    print("✅ Todos los archivos de dependencias encontrados")
    return True


def main():
    print("\n" + "="*60)
    print("🔧 PARCHE AUTOMÁTICO DE GUI - FUNCIONALIDADES HÍBRIDAS")
    print("="*60)
    print()

    # Verificar dependencias
    print("📦 Verificando dependencias...")
    if not verify_dependencies():
        print("\n❌ Faltan archivos necesarios. Instala todos los archivos primero.")
        return 1

    print()

    # Preguntar confirmación
    response = input("¿Deseas parchear src/gui.py? (Se creará backup) [S/n]: ").strip().lower()
    if response and response not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada por el usuario")
        return 0

    print()

    # Parchear
    if patch_gui():
        print("\n🎉 ¡Parche completado exitosamente!")
        print("\nEjecuta: python run_gui.py")
        return 0
    else:
        print("\n❌ Error al parchear. Revisa los backups.")
        return 1


if __name__ == "__main__":
    exit(main())
