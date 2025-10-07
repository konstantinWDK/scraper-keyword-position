# 🔍 Keyword Position Scraper - Google API Edition

**POSICIONES DE KEYWORDS USANDO SOLAMENTE GOOGLE CUSTOM SEARCH API**

Alternativa ética y legal 100% Google API - Sin Selenium, Sin proxies, Sin riesgos de bloqueo.

## 🚀 Características

✅ **100% Google API** - Usa Custom Search API oficial de Google
✅ **Sin anti-detección** - API oficial = accesos garantizados
✅ **Sin proxies** - Google maneja las cuotas internacionalmente
✅ **Credenciales persistentes** - API Key y Search Engine ID guardados
✅ **API de calidad** - Posiciones reales de resultados de búsqueda
✅ **Interfaz gráfica moderna** - Configuración guiada paso a paso
✅ **Cuotas claras** - 100 consultas gratis/día, costos predecibles

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
# 🚀 GOOGLE API CONFIGURACIÓN
# Obtén tu API Key: https://console.cloud.google.com/apis/credentials
GOOGLE_API_KEY=tu_api_key_aqui

# Obtén tu Search Engine ID: https://cse.google.com/ (copia después de 'cx=')
GOOGLE_SEARCH_ENGINE_ID=tu_search_engine_id_aqui

# ➡️ USO DE GOOGLE API (siempre verdadero)
USE_GOOGLE_API=true

# Delays entre keywords (segundos)
MIN_KEYWORD_DELAY=5
MAX_KEYWORD_DELAY=15

# Configuración geográfica
DEFAULT_COUNTRY=US
DEFAULT_LANGUAGE=en
PAGES_TO_SCRAPE=1
```

## 🔧 Uso

### **Interfaz Gráfica (Único método disponible)**
```bash
python run_gui.py
```

### **🌟 Configuración Guiada (Nuevo):**

1. **Configura Google API:**
   - Pestaña "**🔐 Google API**"
   - Ingresa API Key y Search Engine ID
   - Botón "**✅ Validar Credenciales API**"

2. **Carga Keywords:**
   - Pestaña "**🔑 Keywords**"
   - Carga desde archivo o ingresa manualmente
   - Botón "**📁 Cargar desde Archivo**" (usa `keywords_ejemplo.txt`)

3. **Ajusta Configuración:**
   - Pestaña "**⚙️ Configuración**"
   - Configura delays y parámetros geográficos

4. **Ejecuta Scraping:**
   - Pestaña "**🚀 Scraping**"
   - Botón "**🧪 Probar API**" (prueba credenciales)
   - Botón "**🚀 Iniciar Scraping**" (obtén posiciones)
   - Botón "**⏹️ Detener**" (detiene proceso)

### **💡 Uso Recomendado:**

```bash
# Ejecutar aplicación
python run_gui.py

# Flujo típico:
1. Ir a "🔐 Google API" y configurar credenciales
2. Cargar keywords_ejemplo.txt para probar
3. Configurar dominio objetivo (opcional)
4. Presionar "🧪 Probar API"
5. Presionar "🚀 Iniciar Scraping"
6. Ver resultados en pestaña "📊 Resultados"
```

## 📁 Estructura del Proyecto

```
scraper-keyword-position/
├── run_gui.py              # 🚀 punto de entrada principal
├── src/
│   ├── gui.py              # Interfaz gráfica moderna
│   ├── stealth_scraper.py  # Motor de scraping con Google API
│   └── utils.py             # Utilidades y análisis
├── config/
│   ├── .env                # Configuración de credenciales
│   └── settings.py          # Gestor de configuración
├── data/                   # Resultados exportados
├── logs/                   # Logs del scraper
├── keywords_ejemplo.txt    # Keywords de ejemplo
├── requirements.txt        # Dependencias mínimas
└── README.md               # Esta documentación
```

## 🔍 Cómo Funciona Google Custom Search API

### **📋 Entendiendo el Algoritmo de Posicionamiento**

Este scraper usa la **Google Custom Search JSON API** para obtener resultados de búsqueda idénticos a los de Google.com:

#### **1. 🚀 Proceso de API:**

1. **Consulta API:** `serp_scraper_api(keyword)` hace llamadas REST a Google
2. **Parámetros:** Se configura página, país, idioma (geolocalización)
3. **Resultado:** Obtiene JSON con top 10 resultados por página
4. **Posicionamiento:** Asigna posiciones secuenciales (1, 2, 3... por cada página)

#### **2. 📊 Ejemplo Técnico - Keyword "marketing digital":**

```javascript
// Llamada real a Google API:
fetch('https://www.googleapis.com/customsearch/v1?key=TU_API_KEY&cx=TU_SEARCH_ENGINE_ID&q=marketing+digital&start=1&num=10&gl=US&hl=en')
  .then(response => response.json())
  .then(data => {
    // Resultados de búsqueda reales
    data.items.forEach((item, index) => {
      // index: 0, 1, 2, 3... (posiciones físicas)
      console.log(`${index + 1}: ${item.title} - ${item.link}`)
    })
  })
```

#### **3. 📈 Cálculo de Posiciones:**

```
Página 1 (posiciones 1-10):
  + Resultado 1: pos = 1
  + Resultado 2: pos = 2
  + ...
  + Resultado 10: pos = 10

Página 2 (posiciones 11-20):
  + Resultado 1: pos = 11
  + Resultado 2: pos = 2
  + ...
  + Resultado 10: pos = 20
```

### **🎯 Diferencia con Scraping Directo:**

✅ **Google API:**
- Resultados **idénticos** a Google.com
- Posiciones **calculadas correctamente**
- Sin problemas de bloqueo o detección
- Acceso garantizado

❌ **Scraping Directo (Técnica Antigua):**
- Podía obtener solo resultados visibles
- Riesgo de resultados incompletos
- Dependía del navegador y proxies
- Mayor riesgo de bloqueo

## 📊 Formatos de Salida

### CSV
```csv
keyword,position,title,url,domain,page,snippet
"marketing digital",3,"Cómo Hacer Marketing Digital - Guía Completa","https://example.com/guia","example.com",1,"Aprende todas las técnicas..."
```

### JSON
```json
[
  {
    "keyword": "marketing digital",
    "position": 3,
    "title": "Cómo Hacer Marketing Digital - Guía Completa",
    "url": "https://example.com/guia",
    "domain": "example.com",
    "page": 1,
    "snippet": "Aprende todas las técnicas de marketing digital en este guide completo..."
  }
]
```

## 🔍 Análisis de Resultados

En la aplicación gráfica, ve a pestaña "**📈 Análisis**" para generar gráficos automáticamente:

### Métricas incluidas:
- 📊 **Distribución de posiciones** - TOP 3, TOP 10, distribución general
- 🏆 **Top dominios** - Mejores posiciones por dominio
- 📈 **Resultados por página** - Crecimiento de posiciones paginadas
- 💡 **Boxplot de posiciones** - Estadísticas visuales
- 🏅 **Ranking por keywords** - Mejores posiciones por término

### Exportación automática:
- **CSV** y **JSON** con métricas completas
- Gráficos de distribución disponibles
- Históricos de posiciones por dominio

## 🚨 Notas Importantes

### ⚖️ Uso Responasable con Google API
- ✅ **Recomendado** - API oficial de Google
- 📊 **Cuotas transparentes** - 100 consultas/día gratis
- 🔒 **Sin bloqueos** - API garantizada
- 💰 **Costos claros** - $5 por cada 1000 consultas adicionales

### 📢 Recordatorios de API
- **🔑 API Key** segura - No shares tu clave
- **⚡ Rate Limiting** - Respeta los límites de Google
- **🌐 Geolocalización** - Resultados por país/idioma
- **🔄 Cuotas reset** - Se rellenan cada día

### 💡 Recomendaciones por Volumen
```python
# Para PROYECTOS PEQUEÑOS (≤100 keywords/día):
➡️ Configurar delays 5-15s (predeterminado)
➡️ Ideal para clientes personales

# Para CAMPANÍAS MEDIANAS (100-500 keywords/día):
➡️ Ubgrapes 100 consultas gratis diarias
➡️ Usar delays de 2-5s

# Para EMPRESAS GRANDES (>500 keywords/día):
➡️ Solo keywords estratégicas
➡️ $5 por cada 1000 consultas adicionales
```

### 🔧 Solución de Problemas

#### 🔐 Problemas de Credenciales
**"Sin API Key/Modelo Search Engine ID"**
- ✅ Verifica la pestaña "**🔐 Google API**"
- ✅ Asegúrate que la API Key empiece por `AIza`...
- ✅ El Search Engine ID debe ser similar a `e1afc530d3cd24be5`

**"Error 403: Forbidden"**
- ✅ El Search Engine ID no coincide con tu API Key
- ✅ Verifica que ambas credenciales sean de la misma cuenta

#### 📊 Problemas de Cuotas Google
**"DAILY_LIMIT_EXCEEDED"**
- ✅ Has agotado las 100 consultas diarias gratis
- ✅ Espera al día siguiente para reset automático
- ✅ O actualiza a plan pago

**"429: Too Many Requests"**
- ✅ Google está limitando temporalmente
- ✅ Espera unos minutos y continúa
- ✅ Reduce la frecuencia de consultas

#### 🔍 Problemas de Resultados
**"Sin resultados encontrados"**
- ✅ La keyword es demasiado específica
- ✅ El país/idioma puede no tener resultados
- ✅ Prueba con keywords más genéricos

**"Posiciones inconsistentes"** (normal vs API)
- ✅ Google API da resultados diferentes por usuario/location
- ✅ Las posiciones varían según personalización

#### 🖥️ Problemas Técnicos
**"No se puedo iniciar la aplicación"**
- ✅ Asegúrate de tener instalado CustomTkinter
- ✅ `pip install customtkinter`

**"Error de conexión a Google API"**
- ✅ Verifica tu conexión a internet
- ✅ Usa `ping google.com`

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
