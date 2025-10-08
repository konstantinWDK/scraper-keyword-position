#!/bin/bash

echo "========================================"
echo " Keyword Position Scraper - Linux Build"
echo "========================================"
echo

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python 3.8+ usando tu gestor de paquetes"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "✓ Python3 encontrado"
echo

# Cambiar al directorio padre (donde está requirements.txt)
cd "$(dirname "$0")/.."

# Instalar dependencias
echo "Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de dependencias"
    exit 1
fi

echo "✓ Dependencias instaladas"
echo

# Instalar PyInstaller si no está instalado
echo "Instalando PyInstaller..."
pip3 install pyinstaller
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de PyInstaller"
    exit 1
fi

echo "✓ PyInstaller instalado"
echo

# Cambiar al directorio linux
cd linux

# Compilar la aplicación
echo "Compilando aplicación..."
pyinstaller scraper.spec
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la compilación"
    exit 1
fi

echo
echo "========================================"
echo "✓ Compilación completada exitosamente"
echo "========================================"
echo
echo "El ejecutable se encuentra en: dist/KeywordPositionScraper"
echo

# Hacer el script ejecutable
chmod +x dist/KeywordPositionScraper

echo "✓ Permisos de ejecución configurados"
echo "Para ejecutar: ./dist/KeywordPositionScraper"