# Keyword Position Scraper - Windows Build

## Requisitos Previos

- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)
- Conexión a internet para descargar dependencias

## Instrucciones de Compilación

### Método Automático (Recomendado)

1. Abre una terminal de comandos (cmd) como administrador
2. Navega hasta la carpeta `windows` del proyecto
3. Ejecuta el script de compilación:
   ```cmd
   build_windows.bat
   ```

### Método Manual

1. Instala las dependencias:
   ```cmd
   cd ..
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Regresa a la carpeta windows:
   ```cmd
   cd windows
   ```

3. Compila la aplicación:
   ```cmd
   pyinstaller scraper.spec
   ```

## Resultado

- El ejecutable se generará en: `dist\KeywordPositionScraper.exe`
- Puedes distribuir este archivo junto con la carpeta `dist` completa
- No requiere instalación de Python en el equipo de destino

## Solución de Problemas

### Error: Python no encontrado
- Asegúrate de que Python esté instalado y agregado al PATH del sistema
- Reinicia la terminal después de instalar Python

### Error de dependencias
- Verifica tu conexión a internet
- Ejecuta: `pip install --upgrade pip`
- Intenta instalar las dependencias una por una

### Error de compilación
- Verifica que todas las dependencias estén instaladas
- Asegúrate de tener suficiente espacio en disco (mínimo 500MB)
- Ejecuta como administrador si hay problemas de permisos

## Notas Adicionales

- El proceso de compilación puede tomar varios minutos
- El ejecutable final tendrá un tamaño aproximado de 100-200MB
- Se incluye una consola para depuración (console=True en scraper.spec)