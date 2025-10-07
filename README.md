# 🔍 Keyword Position Scraper - Anti-detección 2025

Scraper avanzado de posiciones de keywords con técnicas anti-detección para Google SERP. Alternativa gratuita a ScrapeBox.

## 🚀 Características

✅ **Anti-detección avanzada** - Undetected Chrome, headers rotativos, comportamiento humano  
✅ **Soporte de proxies** - Rotación automática de proxies  
✅ **Google Suggest** - Generación de keywords con múltiples fuentes  
✅ **Análisis de posiciones** - Tracking completo de rankings  
✅ **Exportación múltiple** - CSV, JSON, análisis estadístico  
✅ **Configuración flexible** - Delays, países, idiomas personalizables  
✅ **Interfaz gráfica** - GUI moderna y fácil de usar

## 📦 Instalación Rápida

### Instalación Automática (Recomendada)
```bash
git clone <tu-repo>
cd scraper-keyword-position
./install
```

### Instalación Manual
```bash
# Solo instalar dependencias (Python ya debe estar instalado)
python setup.py
```

## ⚙️ Configuración

Edita `config/.env`:

```env
# Proxies (Recomendado para evitar bloqueos)
PROXY_1=user:pass@proxy1.com:8080
PROXY_2=proxy2.com:3128

# Delays (segundos)
MIN_KEYWORD_DELAY=5
MAX_KEYWORD_DELAY=15

# Configuración Google
DEFAULT_COUNTRY=US
DEFAULT_LANGUAGE=en
PAGES_TO_SCRAPE=1
```

## 🔧 Uso

### Interfaz Gráfica (Recomendado)
```bash
python src/gui.py
```

### Línea de Comandos

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

### Ejemplos Avanzados

```bash
# Scraping múltiples páginas con salida personalizada
python src/main.py --keywords "seo,sem,marketing" --domain midominio.com --pages 3 --output mis_resultados

# Keywords desde archivo con configuración específica
python src/main.py --keyword-file keywords.txt --domain ejemplo.com --country ES --language es

# Solo generar keywords (sin scraping)
python src/main.py --suggest "marketing digital" --country ES
```

## 📁 Estructura del Proyecto

```
scraper-keyword-position/
├── src/
│   ├── main.py              # Script principal
│   ├── gui.py              # Interfaz gráfica
│   ├── stealth_scraper.py   # Motor de scraping
│   └── utils.py             # Utilidades y análisis
├── config/
│   ├── .env                 # Configuración (crear desde .env.example)
│   ├── .env.example         # Plantilla de configuración
│   └── settings.py          # Gestor de configuración
├── data/                    # Resultados exportados
├── logs/                    # Logs del scraper
├── requirements.txt         # Dependencias
├── setup.py                # Instalador de dependencias
└── install                 # Script de instalación simple
```

## 📊 Formatos de Salida

### CSV
```csv
keyword,position,title,url,domain,page
"marketing digital",3,"Guía Marketing Digital","https://example.com/guia","example.com",1
```

### JSON
```json
{
  "keyword": "marketing digital",
  "position": 3,
  "title": "Guía Marketing Digital",
  "url": "https://example.com/guia",
  "domain": "example.com",
  "page": 1
}
```

## 🔍 Análisis de Resultados

```bash
# Analizar último archivo
python src/main.py --analyze

# Analizar archivo específico
python src/main.py --analyze-file data/positions_ejemplo.csv
```

### Métricas incluidas:
- Posición promedio y mediana
- Distribución TOP 3, TOP 10, Página 2+
- Ranking por dominio
- Keywords con mejores posiciones

## ⚡ Técnicas Anti-detección

### 🛡️ Selenium Stealth
- Undetected ChromeDriver
- Headers realistas rotativos
- User-agents aleatorios
- Window size variable
- JavaScript anti-fingerprinting

### 🔄 Comportamiento Humano
- Delays humanizados variables
- Scroll aleatorio
- Movimientos de mouse
- Pausas micro-aleatorias

### 🌐 Proxies
- Rotación automática
- Soporte HTTP/HTTPS
- Testing automático
- Fallback sin proxy

## 🚨 Notas Importantes

### ⚖️ Uso Responsable
- Solo para investigación legítima
- Respetar robots.txt
- No sobrecargar servidores
- Cumplir términos de servicio

### 💡 Recomendaciones
- Usar proxies premium para volumen alto
- Configurar delays apropiados (5-15s)
- Monitorear logs por bloqueos
- Hacer backups de configuración

### 🔧 Troubleshooting

#### ChromeDriver Issues
```bash
# Actualizar undetected-chromedriver
pip install --upgrade undetected-chromedriver
```

#### Proxy Issues
```bash
# Probar proxies individualmente
python -c "from src.utils import ProxyTester; ProxyTester.test_proxy('tu-proxy:puerto')"
```

#### Rate Limiting
- Aumentar delays en `.env`
- Usar más proxies
- Reducir páginas por keyword

## 📈 Roadmap

- [ ] Integración con APIs SERP
- [ ] Dashboard web
- [ ] Alertas automáticas
- [ ] Base de datos persistente
- [ ] Scraping programado
- [ ] Más fuentes de suggest

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es para uso educativo y de investigación. El usuario es responsable de cumplir con los términos de servicio de los sitios web scrapeados.

## 💬 Soporte

Si encuentras issues:
1. Revisa los logs en `logs/scraper.log`
2. Verifica la configuración con `--config`
3. Prueba con `--test`
4. Abre un issue con detalles del error

---

**⚠️ Disclaimer**: Este scraper es para uso educativo y de investigación. El uso responsable es responsabilidad del usuario.
