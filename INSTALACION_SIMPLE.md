# 🔧 Instalación Rápida - Keyword Position Scraper

## Prerrequisitos
- ✅ Python 3.8+ instalado
- ✅ Google Chrome instalado
- ✅ pip actualizado

## Instalación en 3 pasos

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar entorno
```bash
# Copiar configuración de ejemplo
cp config/.env.example config/.env

# Crear directorios necesarios
mkdir -p data logs
```

### 3. Verificar instalación
```bash
# Probar CLI
python src/main.py --test

# O iniciar GUI
python src/gui.py
```

## Dependencias instaladas

El archivo `requirements.txt` incluye:
- **selenium** - Automatización web
- **undetected-chromedriver** - ChromeDriver indetectable
- **customtkinter** - Interfaz gráfica moderna
- **pandas** - Análisis de datos
- **matplotlib** - Gráficos y visualización
- **requests** - Peticiones HTTP
- **beautifulsoup4** - Parseo HTML
- **fake-useragent** - User-agents rotativos

## Uso Rápido

### Interfaz Gráfica (Recomendado)
```bash
python src/gui.py
```

### Línea de Comandos
```bash
# Modo prueba
python src/main.py --test

# Scraping básico
python src/main.py --keywords "seo,marketing" --domain ejemplo.com

# Desde archivo
python src/main.py --keyword-file keywords.txt --domain ejemplo.com

# Google Suggest
python src/main.py --suggest "marketing" --country ES
```

## Configuración

Edita `config/.env` para personalizar:
- Proxies
- Delays entre requests
- País e idioma
- Número de páginas

## Solución de Problemas

### Error: ChromeDriver no encontrado
```bash
pip install --upgrade undetected-chromedriver
```

### Error: Módulos faltantes
```bash
pip install setuptools
```

### Error: Permisos
```bash
# En Linux/Mac
chmod +x install.sh
```

## Estructura del Proyecto
```
scraper-keyword-position/
├── src/           # Código fuente
├── config/        # Configuración
├── data/          # Resultados
├── logs/          # Logs
└── requirements.txt
```

¡Listo! Tu scraper está configurado y listo para usar. 🚀
