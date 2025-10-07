#!/bin/bash

# Script de instalación para Keyword Position Scraper
# Anti-detección 2025 con GUI

echo "🔧 Instalando Keyword Position Scraper..."
echo "=========================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instala pip3."
    exit 1
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🚀 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "🔄 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p data logs

# Configurar archivo de entorno
echo "⚙️ Configurando variables de entorno..."
if [ ! -f "config/.env" ]; then
    cp config/.env.example config/.env
    echo "✅ Archivo .env creado desde plantilla"
else
    echo "ℹ️  Archivo .env ya existe"
fi

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "
import sys
try:
    import selenium
    import undetected_chromedriver
    import customtkinter
    import pandas
    import matplotlib
    print('✅ Todas las dependencias instaladas correctamente')
except ImportError as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"

# Instalar ChromeDriver automáticamente
echo "🌐 Configurando ChromeDriver..."
python -c "
import undetected_chromedriver as uc
try:
    driver = uc.Chrome()
    driver.quit()
    print('✅ ChromeDriver configurado correctamente')
except Exception as e:
    print(f'⚠️  ChromeDriver necesita configuración manual: {e}')
"

echo ""
echo "🎉 Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Edita config/.env con tu configuración"
echo "   2. Para usar la GUI: python src/gui.py"
echo "   3. Para usar CLI: python src/main.py --help"
echo ""
echo "🚀 Para iniciar la GUI:"
echo "   source venv/bin/activate"
echo "   python src/gui.py"
echo ""
echo "💡 Para más información, consulta README_COMPLETO.md"
