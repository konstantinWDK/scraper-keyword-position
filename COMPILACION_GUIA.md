# Guía de Compilación - Keyword Position Scraper

Esta guía explica cómo compilar y ejecutar el Keyword Position Scraper en Linux y Windows.

## 📋 Requisitos Previos

### Para Linux
- Python 3.8 o superior
- tkinter (normalmente incluido con Python)
- pip (gestor de paquetes de Python)

### Para Windows  
- Python 3.8 o superior
- tkinter (viene incluido con Python en Windows)
- pip (gestor de paquetes de Python)

## 🐧 Compilación en Linux

### 1. Preparación del sistema
```bash
# En Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-tk

# En CentOS/RHEL:
sudo yum install python3 python3-pip python3-tkinter

# En Arch Linux:
sudo pacman -S python python-pip tk
```

### 2. Compilar la aplicación
```bash
# Navegar al directorio del proyecto
cd scraper-keyword-position

# Ejecutar el script de compilación
./linux/build_linux.sh
```

### 3. Ejecutar la aplicación
```bash
# Opción 1: Usar el script de lanzamiento (recomendado)
./run_scraper.sh

# Opción 2: Ejecutar directamente
./linux/dist/KeywordPositionScraper
```

## 🪟 Compilación en Windows

### 1. Preparación del sistema
- Descargar Python desde [python.org](https://python.org)
- **IMPORTANTE**: Durante la instalación, marcar la opción **"Add Python to PATH"**
- tkinter viene incluido automáticamente

### 2. Compilar la aplicación
```cmd
# Abrir CMD o PowerShell como administrador
# Navegar al directorio del proyecto
cd scraper-keyword-position

# Ejecutar el script de compilación
windows\build_windows.bat
```

### 3. Ejecutar la aplicación
```cmd
# Opción 1: Usar el script de lanzamiento (recomendado)
run_scraper.bat

# Opción 2: Ejecutar directamente
windows\dist\KeywordPositionScraper.exe
```

## 🔧 Características de los Scripts de Compilación Mejorados

### Para Linux (`build_linux.sh`)
- ✅ Verifica que Python 3 esté instalado
- ✅ Verifica que tkinter esté disponible
- ✅ Crea entorno virtual para evitar conflictos
- ✅ Actualiza pip automáticamente
- ✅ Instala todas las dependencias
- ✅ Compila con PyInstaller optimizado
- ✅ Crea script de lanzamiento para usuario
- ✅ Configura permisos de ejecución
- ✅ Limpia entorno virtual opcionalmente

### Para Windows (`build_windows.bat`)
- ✅ Verifica que Python esté instalado y en PATH
- ✅ Verifica que tkinter esté disponible
- ✅ Crea entorno virtual para evitar conflictos
- ✅ Actualiza pip automáticamente
- ✅ Instala todas las dependencias
- ✅ Compila con PyInstaller optimizado
- ✅ Crea script de lanzamiento para usuario
- ✅ Maneja correctamente rutas de Windows
- ✅ Limpia entorno virtual opcionalmente

## 📦 Archivos Generados

### Después de la compilación exitosa:

#### En Linux:
- `linux/dist/KeywordPositionScraper` - Ejecutable principal
- `run_scraper.sh` - Script de lanzamiento para usuario

#### En Windows:
- `windows/dist/KeywordPositionScraper.exe` - Ejecutable principal
- `run_scraper.bat` - Script de lanzamiento para usuario

## 🚀 Ejecución a Nivel de Usuario

La aplicación está diseñada para ejecutarse sin privilegios de administrador:

### Linux:
```bash
# Desde cualquier ubicación del proyecto
./run_scraper.sh

# O copiar el ejecutable a una ubicación del PATH
sudo cp linux/dist/KeywordPositionScraper /usr/local/bin/
# Luego ejecutar desde cualquier lugar:
KeywordPositionScraper
```

### Windows:
```cmd
# Desde cualquier ubicación del proyecto
run_scraper.bat

# O crear un acceso directo al ejecutable
# Click derecho en KeywordPositionScraper.exe → "Crear acceso directo"
# Mover el acceso directo al escritorio o menú inicio
```

## 🔍 Solución de Problemas Comunes

### Error: "tkinter no encontrado"
**Linux:**
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo yum install python3-tkinter  # CentOS/RHEL
sudo pacman -S tk  # Arch Linux
```

**Windows:**
- Reinstalar Python marcando "Add Python to PATH"
- Verificar que tkinter esté incluido en la instalación

### Error: "Python no encontrado"
**Linux:**
```bash
# Verificar instalación
python3 --version
# Si no está instalado:
sudo apt install python3  # Ubuntu/Debian
```

**Windows:**
- Verificar que Python esté en el PATH
- Reinstalar Python marcando "Add Python to PATH"

### Error de dependencias durante compilación
- Los scripts crean un entorno virtual automáticamente
- Si hay conflictos, eliminar `build_env/` y ejecutar de nuevo

### La aplicación se cierra inesperadamente
- Verificar que todas las dependencias estén incluidas
- Ejecutar desde terminal para ver mensajes de error
- Verificar que haya suficiente memoria disponible

## 📊 Estructura del Proyecto

```
scraper-keyword-position/
├── linux/
│   ├── build_linux.sh          # Script de compilación Linux
│   ├── scraper.spec            # Configuración PyInstaller Linux
│   └── dist/                   # Ejecutable generado (después de compilar)
├── windows/
│   ├── build_windows.bat       # Script de compilación Windows
│   ├── scraper.spec            # Configuración PyInstaller Windows
│   └── dist/                   # Ejecutable generado (después de compilar)
├── src/                        # Código fuente
├── config/                     # Configuraciones
├── data/                       # Datos de la aplicación
├── logs/                       # Archivos de log
├── projects/                   # Proyectos guardados
├── reports/                    # Reportes generados
├── run_scraper.sh              # Script de lanzamiento Linux
├── run_scraper.bat             # Script de lanzamiento Windows
└── requirements.txt            # Dependencias de Python
```

## 🔄 Actualización

Para actualizar la aplicación:

1. **Obtener la última versión:**
   ```bash
   git pull origin main
   ```

2. **Recompilar:**
   ```bash
   # Linux
   ./linux/build_linux.sh
   
   # Windows
   windows\build_windows.bat
   ```

3. **La aplicación estará actualizada y lista para usar.**

## 📞 Soporte

Si encuentras problemas durante la compilación o ejecución:

1. Verifica que todos los requisitos estén instalados
2. Ejecuta los scripts desde terminal/CMD para ver mensajes de error
3. Revisa los logs en `logs/scraper.log`
4. Asegúrate de tener permisos de ejecución en Linux

¡La aplicación está lista para usar! 🎉
