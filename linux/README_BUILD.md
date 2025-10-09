# Keyword Position Scraper - Linux Build

## Requisitos Previos

- Python 3.8 o superior
- pip3 (gestor de paquetes de Python)
- Conexión a internet para descargar dependencias

### Instalación de Python (si no está instalado)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install python3 python3-pip
# o para versiones más antiguas:
# sudo yum install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

## Instrucciones de Compilación

### Método Automático (Recomendado)

1. Abre una terminal
2. Navega hasta la carpeta `linux` del proyecto
3. Da permisos de ejecución al script:
   ```bash
   chmod +x build_linux.sh
   ```
4. Ejecuta el script de compilación:
   ```bash
   ./build_linux.sh
   ```

### Método Manual

1. Instala las dependencias:
   ```bash
   cd ..
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   ```

2. Regresa a la carpeta linux:
   ```bash
   cd linux
   ```

3. Compila la aplicación:
   ```bash
   pyinstaller scraper.spec
   ```

4. Da permisos de ejecución:
   ```bash
   chmod +x dist/KeywordPositionScraper
   ```

## Resultado

- El ejecutable se generará en: `dist/KeywordPositionScraper`
- Puedes distribuir este archivo junto con la carpeta `dist` completa
- No requiere instalación de Python en el equipo de destino

## Ejecución

```bash
./dist/KeywordPositionScraper
```

## Solución de Problemas

### Error: Python3 no encontrado
- Instala Python3 usando el gestor de paquetes de tu distribución
- Verifica la instalación: `python3 --version`

### Error de dependencias
- Verifica tu conexión a internet
- Actualiza pip: `pip3 install --upgrade pip`
- En algunas distribuciones necesitas: `sudo apt install python3-dev`

### Error de compilación
- Verifica que todas las dependencias estén instaladas
- Asegúrate de tener suficiente espacio en disco (mínimo 500MB)
- Instala dependencias del sistema si es necesario:
  ```bash
  sudo apt install python3-tk python3-dev
  ```

### Error de permisos
- Ejecuta con sudo si es necesario para instalar dependencias
- Asegúrate de que el script tenga permisos de ejecución

## Dependencias del Sistema

Algunas distribuciones pueden requerir paquetes adicionales:

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk python3-dev build-essential
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install tkinter python3-devel gcc
```

## Notas Adicionales

- El proceso de compilación puede tomar varios minutos
- El ejecutable final tendrá un tamaño aproximado de 100-200MB
- Se incluye una consola para depuración
- Compatible con la mayoría de distribuciones Linux x86_64