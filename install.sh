#!/bin/bash

echo "🚀 Instalando scraper-keyword-position..."

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivos de configuración si no existen
if [ ! -f config/.env ]; then
    cp config/.env.example config/.env
    echo "📝 Configura tus proxies en config/.env"
fi

echo "✅ Instalación completada!"
echo "📖 Para usar:"
echo "   source venv/bin/activate"
echo "   python src/main.py"