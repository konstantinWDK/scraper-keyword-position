#!/bin/bash

echo "========================================"
echo " Keyword Position Scraper - Linux Build"
echo "========================================"
echo

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python 3.8+ usando tu gestor de paquetes"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip python3-tkinter"
    echo "Arch: sudo pacman -S python python-pip tk"
    exit 1
fi

echo "✓ Python3 encontrado"
echo

# Verificar que tkinter está instalado (necesario para GUI)
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: tkinter no está instalado"
    echo "Por favor instala tkinter usando tu gestor de paquetes"
    echo "Ubuntu/Debian: sudo apt install python3-tk"
    echo "CentOS/RHEL: sudo yum install python3-tkinter"
    echo "Arch: sudo pacman -S tk"
    exit 1
fi
echo "✓ tkinter encontrado"
echo

# Cambiar al directorio padre (donde está requirements.txt)
cd "$(dirname "$0")/.."

# Crear entorno virtual para evitar conflictos
echo "Creando entorno virtual..."
python3 -m venv build_env
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la creación del entorno virtual"
    exit 1
fi

# Activar entorno virtual
source build_env/bin/activate

echo "✓ Entorno virtual creado y activado"
echo

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la actualización de pip"
    exit 1
fi

echo "✓ pip actualizado"
echo

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de dependencias"
    exit 1
fi

echo "✓ Dependencias instaladas"
echo

# Instalar PyInstaller si no está instalado
echo "Instalando PyInstaller..."
pip install pyinstaller
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
pyinstaller scraper.spec --clean
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

# Crear script de lanzamiento para usuario
echo "Creando script de lanzamiento para usuario..."
cat > ../run_scraper.sh << 'EOF'
#!/bin/bash
# Script de lanzamiento para Keyword Position Scraper
# Este script puede ejecutarse desde cualquier ubicación

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
"$SCRIPT_DIR/linux/dist/KeywordPositionScraper"
EOF

chmod +x ../run_scraper.sh

echo "✓ Script de lanzamiento creado: run_scraper.sh"
echo
echo "Para ejecutar la aplicación:"
echo "  ./run_scraper.sh"
echo
echo "O directamente:"
echo "  ./linux/dist/KeywordPositionScraper"
echo
echo "La aplicación está lista para usar a nivel de usuario."

# Desactivar entorno virtual
deactivate

# Limpiar entorno virtual (opcional)
echo "¿Deseas eliminar el entorno virtual de compilación? (s/N)"
read -r response
if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
    rm -rf ../build_env
    echo "✓ Entorno virtual eliminado"
fi
