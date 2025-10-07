# 🔍 Keyword Position Scraper - Anti-detección 2025

## 📋 Tabla de Contenidos
- [Descripción](#-descripción)
- [Características](#-características)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Interfaz Gráfica](#-interfaz-gráfica)
- [API](#-api)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## 🎯 Descripción

Scraper avanzado de posiciones de keywords en Google SERP con técnicas de anti-detección avanzadas. Diseñado para SEOs, marketers y desarrolladores que necesitan monitorear posiciones de manera eficiente y discreta.

**Alternativa gratuita a herramientas premium como ScrapeBox, Ahrefs y SEMrush.**

## ✨ Características

### 🛡️ Anti-detección Avanzada
- **Undetected ChromeDriver** - Navegador indetectable
- **Headers rotativos** - User-agents y headers realistas
- **Comportamiento humano** - Delays variables, scroll aleatorio, movimientos de mouse
- **JavaScript anti-fingerprinting** - Scripts para evadir detección
- **Window size variable** - Resoluciones aleatorias

### 🔄 Gestión de Proxies
- **Rotación automática** - Cambio inteligente entre proxies
- **Soporte múltiple** - HTTP/HTTPS, con/sin autenticación
- **Testing automático** - Verificación de proxies funcionales
- **Fallback seguro** - Continuación sin proxy si es necesario

### 🔍 Funcionalidades de Scraping
- **SERP scraping** - Extracción completa de resultados de búsqueda
- **Google Suggest** - Generación automática de keywords
- **Búsqueda por dominio** - Tracking específico de competidores
- **Múltiples páginas** - Scraping de hasta 10 páginas por keyword
- **Análisis en tiempo real** - Estadísticas y métricas inmediatas

### 📊 Análisis y Exportación
- **Múltiples formatos** - CSV, JSON, análisis estadístico
- **Dashboard visual** - Gráficos y métricas interactivas
- **Comparativas** - Evolución de posiciones en el tiempo
- **Alertas automáticas** - Notificaciones de cambios importantes

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- Google Chrome instalado
- Conexión a internet
- (Opcional) Proxies para scraping masivo

### Instalación Automática (Recomendada)

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/scraper-keyword-position.git
cd scraper-keyword-position

# Ejecutar script de instalación
chmod +x install.sh
./install.sh
```

### Instalación Manual

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp config/.env.example config/.env
```

### Verificar Instalación

```bash
# Probar instalación
python src/main.py --test

# Verificar configuración
python src/main.py --config
```

## ⚙️ Configuración

### Archivo de Configuración (.env)

Edita `config/.env` con tus preferencias:

```env
# ========== PROXIES ==========
# Formato: usuario:password@ip:puerto o ip:puerto
PROXY_1=user:pass@proxy1.com:8080
PROXY_2=proxy2.com:3128
PROXY_3=192.168.1.100:8080

# ========== DELAYS ==========
# Tiempos en segundos entre requests
MIN_KEYWORD_DELAY=5
MAX_KEYWORD_DELAY=15
MIN_PAGE_DELAY=3
MAX_PAGE_DELAY=8

# ========== GOOGLE ==========
DEFAULT_COUNTRY=US
DEFAULT_LANGUAGE=en
PAGES_TO_SCRAPE=1

# ========== LOGS ==========
LOG_LEVEL=INFO

# ========== RESULTADOS ==========
SAVE_JSON=true
SAVE_CSV=true

# ========== USER AGENTS ==========
CUSTOM_USER_AGENTS=
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
```

### Configuración Recomendada

| Escenario | Min Delay | Max Delay | Proxies | Páginas |
|-----------|-----------|-----------|---------|---------|
| **Testing** | 3s | 8s | 0-1 | 1 |
| **Producción** | 5s | 15s | 3-5 | 1-2 |
| **Masivo** | 8s | 20s | 10+ | 1 |

## 🔧 Uso

### Interfaz de Línea de Comandos

#### Comandos Básicos

```bash
# Modo de prueba
python src/main.py --test

# Keywords específicas
python src/main.py --keywords "seo,marketing digital" --domain example.com

# Desde archivo
python src/main.py --keyword-file keywords.txt --domain example.com --pages 2

# Google Suggest
python src/main.py --suggest "marketing" --country ES --language es

# Análisis de resultados
python src/main.py --analyze
```

#### Comandos Avanzados

```bash
# Scraping múltiples páginas con salida personalizada
python src/main.py --keywords "seo,sem,marketing" --domain midominio.com --pages 3 --output mis_resultados

# Procesamiento por lotes
python src/main.py --batch keywords.txt --domain ejemplo.com --country ES --language es

# Solo generar keywords (sin scraping)
python src/main.py --suggest "marketing digital" --country ES --no-scrape

# Análisis de archivo específico
python src/main.py --analyze-file data/positions_20241201_143022.csv
```

### Interfaz Gráfica (GUI)

```bash
# Iniciar interfaz gráfica
python src/gui.py
```

La GUI ofrece:
- **Configuración visual** - Ajustes con interfaz intuitiva
- **Gestión de keywords** - Carga y edición visual
- **Monitoreo en tiempo real** - Progreso y estadísticas
- **Visualización de resultados** - Gráficos y tablas interactivas
- **Exportación fácil** - Botones de exportación directa

## 🖥️ Interfaz Gráfica

### Características de la GUI

1. **Panel de Configuración**
   - Ajustes de delays y proxies
   - Configuración de país e idioma
   - Opciones de exportación

2. **Gestor de Keywords**
   - Carga desde archivo
   - Edición directa
   - Generación con Google Suggest

3. **Monitor de Progreso**
   - Barra de progreso en tiempo real
   - Estadísticas actualizadas
   - Logs de actividad

4. **Visualizador de Resultados**
   - Tablas interactivas
   - Gráficos de distribución
   - Filtros y búsqueda

5. **Exportación**
   - Formatos múltiples (CSV, JSON, Excel)
   - Configuración personalizada
   - Compartir resultados

### Inicio Rápido con GUI

1. **Iniciar la aplicación:**
   ```bash
   python src/gui.py
   ```

2. **Configurar parámetros:**
   - Dominio objetivo
   - Número de páginas
   - Delays entre requests

3. **Cargar keywords:**
   - Desde archivo o manualmente
   - Generar con Google Suggest

4. **Ejecutar scraping:**
   - Monitorear progreso
   - Ver resultados en tiempo real

5. **Exportar resultados:**
   - Elegir formato
   - Descargar archivos

## 📊 API

### Uso Programático

```python
from stealth_scraper import StealthSerpScraper
from config.settings import config

# Inicializar scraper
scraper = StealthSerpScraper(config)

# Scraping básico
keywords = ["seo", "marketing digital"]
results = scraper.batch_position_check(keywords, "example.com", pages=1)

# Google Suggest
suggestions = scraper.google_suggest_scraper("marketing", country="ES", language="es")

# Análisis
from utils import ResultsAnalyzer
analyzer = ResultsAnalyzer()
stats = analyzer.analyze_file("data/positions.csv")
```

### Ejemplos de Integración

```python
# Integración con base de datos
import sqlite3
from stealth_scraper import StealthSerpScraper

def save_to_database(results):
    conn = sqlite3.connect('positions.db')
    cursor = conn.cursor()
    
    for result in results:
        cursor.execute('''
            INSERT OR REPLACE INTO positions 
            (keyword, position, domain, timestamp) 
            VALUES (?, ?, ?, datetime('now'))
        ''', (result['keyword'], result['position'], result['domain']))
    
    conn.commit()
    conn.close()

# Uso
scraper = StealthSerpScraper(config)
results = scraper.batch_position_check(keywords, target_domain, pages=1)
save_to_database(results)
```

## 🚨 Troubleshooting

### Problemas Comunes

#### ChromeDriver Issues
```bash
# Actualizar undetected-chromedriver
pip install --upgrade undetected-chromedriver

# Verificar versión de Chrome
google-chrome --version

# Forzar reinstalación
pip uninstall undetected-chromedriver
pip install undetected-chromedriver
```

#### Proxy Issues
```bash
# Probar proxies individualmente
python -c "from src.utils import ProxyTester; ProxyTester.test_proxy('tu-proxy:puerto')"

# Probar lista completa
python -c "from src.utils import ProxyTester; ProxyTester.test_proxy_list(['proxy1:port', 'proxy2:port'])"
```

#### Rate Limiting
- **Síntomas**: CAPTCHAs, bloqueos, resultados vacíos
- **Soluciones**:
  - Aumentar delays en `.env`
  - Usar más proxies
  - Reducir páginas por keyword
  - Cambiar user-agents

#### Performance Lenta
- **Causas**: Muchas keywords, proxies lentos, delays altos
- **Optimizaciones**:
  - Usar proxies premium
  - Ajustar delays según necesidad
  - Scrapear solo 1 página por defecto

### Logs y Debugging

```bash
# Ver logs en tiempo real
tail -f logs/scraper.log

# Nivel de debug
LOG_LEVEL=DEBUG
```

## ❓ FAQ

### ¿Es legal usar este scraper?
**Sí**, para investigación legítima y análisis SEO. Respetar siempre:
- `robots.txt` de los sitios
- Términos de servicio
- No sobrecargar servidores

### ¿Cuántas keywords puedo scrapear?
- **Sin proxies**: 50-100 keywords/día
- **Con proxies**: 500-1000 keywords/día
- **Masivo**: 5000+ keywords/día (con infraestructura adecuada)

### ¿Cómo evitar bloqueos?
1. Usar proxies rotativos
2. Configurar delays apropiados (5-15s)
3. Rotar user-agents
4. Monitorear logs constantemente

### ¿Qué formatos de exportación soporta?
- CSV (compatible con Excel, Google Sheets)
- JSON (para análisis programático)
- Análisis estadístico (métricas automáticas)

### ¿Puedo programar scraping automático?
Sí, usando cron jobs o servicios como:
```bash
# Ejemplo de cron job diario
0 2 * * * cd /ruta/al/scraper && python src/main.py --keyword-file keywords.txt --domain ejemplo.com
```

## 🤝 Contribución

### Cómo Contribuir

1. **Fork** el proyecto
2. **Crea una rama** (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. **Push** rama (`git push origin feature/nueva-funcionalidad`)
5. **Crea Pull Request**

### Estructura del Código

```
scraper-keyword-position/
├── src/
│   ├── main.py              # CLI principal
│   ├── gui.py              # Interfaz gráfica
│   ├── stealth_scraper.py  # Motor de scraping
│   └── utils.py            # Utilidades
├── config/
│   ├── settings.py         # Gestor de configuración
│   └── .env               # Variables de entorno
├── data/                  # Resultados
├── logs/                  # Logs de actividad
└── tests/                 # Tests unitarios
```

### Desarrollo

```bash
# Configurar entorno de desarrollo
git clone <repo>
cd scraper-keyword-position
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependencias de desarrollo

# Ejecutar tests
python -m pytest tests/

# Verificar código
flake8 src/
black src/
```

## 🔄 Gestión de Proxies

### Proxies Gratuitos

El proyecto incluye una lista de proxies gratuitos en `proxies_gratuitos.txt` con opciones de:
- **Alta velocidad** - Para scraping básico
- **Diferentes regiones** - Europa, Estados Unidos, Asia
- **Múltiples protocolos** - HTTP, HTTPS, SOCKS5

### Configuración Rápida

1. **Cargar proxies desde archivo:**
   ```bash
   # En la GUI, usar el botón "Cargar desde Archivo" en la pestaña de configuración
   # O editar manualmente config/.env
   ```

2. **Probar proxies:**
   ```bash
   python -c "from src.utils import ProxyTester; ProxyTester.test_proxy_list(['51.158.68.68:8811', '188.166.59.17:8888'])"
   ```

3. **Configurar en .env:**
   ```env
   PROXY_1=51.158.68.68:8811
   PROXY_2=188.166.59.17:8888
   PROXY_3=185.162.251.147:80
   ```

### Recomendaciones de Uso

- **Scraping básico**: 3-5 proxies de alta velocidad
- **Scraping masivo**: 10+ proxies con rotación automática
- **Monitoreo**: Revisar logs frecuentemente por bloqueos
- **Actualización**: Los proxies gratuitos cambian frecuentemente

## 📄 Licencia

Este proyecto es de código abierto para uso educativo y de investigación. El usuario es responsable de cumplir con los términos de servicio de los sitios web scrapeados.

**⚠️ Disclaimer**: Este scraper es para uso educativo y de investigación. El uso responsable es responsabilidad del usuario.

## 📞 Soporte

### Canales de Ayuda

1. **Documentación**: Revisa este README y los comentarios en el código
2. **Issues**: Reporta bugs en GitHub Issues
3. **Comunidad**: Únete a nuestro Discord/Telegram
4. **Email**: soporte@tudominio.com

### Información para Reportar Issues

Al reportar un problema, incluye:
- Versión de Python y Chrome
- Configuración usada (sin credenciales)
- Logs relevantes
- Pasos para reproducir
- Comportamiento esperado vs actual

---

**¿Te gusta este proyecto? ⭐ Dale una estrella en GitHub!**
