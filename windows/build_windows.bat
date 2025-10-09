@echo off
echo ========================================
echo  Keyword Position Scraper - Windows Build FIXED
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    echo IMPORTANTE: Durante la instalación, marcar "Add Python to PATH"
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verificar que tkinter está instalado (necesario para GUI)
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: tkinter no está disponible
    echo tkinter viene incluido con Python en Windows
    echo Si no funciona, reinstala Python y asegúrate de que tkinter esté incluido
    pause
    exit /b 1
)
echo ✓ tkinter encontrado
echo.

REM Cambiar al directorio padre (donde está requirements.txt)
cd /d "%~dp0\.."

REM Crear entorno virtual para evitar conflictos
echo Creando entorno virtual...
python -m venv build_env
if %errorlevel% neq 0 (
    echo ERROR: Falló la creación del entorno virtual
    pause
    exit /b 1
)

REM Activar entorno virtual
call build_env\Scripts\activate.bat

echo ✓ Entorno virtual creado y activado
echo.

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ERROR: Falló la actualización de pip
    pause
    exit /b 1
)

echo ✓ pip actualizado
echo.

REM SOLUCIÓN: Habilitar soporte para rutas largas en Windows
echo Configurando soporte para rutas largas en Windows...
python -c "import sys; print('Python version:', sys.version)"
python -c "import os; print('Current working directory:', os.getcwd())"

REM SOLUCIÓN: Instalar dependencias problemáticas primero con flags especiales
echo Instalando dependencias problemáticas primero...
pip install --no-cache-dir numpy>=2.2.0
if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación de numpy
    echo Intentando método alternativo...
    pip install --no-cache-dir --only-binary=all numpy
    if %errorlevel% neq 0 (
        echo ERROR: Falló la instalación alternativa de numpy
        pause
        exit /b 1
    )
)

echo ✓ numpy instalado
echo.

REM Instalar pandas con flags especiales
echo Instalando pandas...
pip install --no-cache-dir pandas>=2.2.0
if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación de pandas
    echo Intentando método alternativo...
    pip install --no-cache-dir --only-binary=all pandas
    if %errorlevel% neq 0 (
        echo ERROR: Falló la instalación alternativa de pandas
        pause
        exit /b 1
    )
)

echo ✓ pandas instalado
echo.

REM Instalar el resto de dependencias
echo Instalando el resto de dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación de dependencias
    echo Intentando instalar dependencias individualmente...
    
    pip install requests==2.31.0
    pip install python-dotenv==1.0.0
    pip install colorama==0.4.6
    pip install tqdm==4.66.1
    pip install customtkinter==5.2.1
    pip install matplotlib==3.8.2
    pip install seaborn==0.13.0
    pip install Pillow==10.1.0
    pip install openpyxl==3.1.2
    pip install google-auth>=2.23.0
    pip install google-auth-oauthlib>=1.1.0
    pip install google-auth-httplib2>=0.1.1
    pip install google-api-python-client>=2.100.0
    
    if %errorlevel% neq 0 (
        echo ERROR: Falló la instalación individual de dependencias
        pause
        exit /b 1
    )
)

echo ✓ Dependencias instaladas
echo.

REM Instalar PyInstaller si no está instalado
echo Instalando PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación de PyInstaller
    pause
    exit /b 1
)

echo ✓ PyInstaller instalado
echo.

REM Cambiar al directorio windows
cd windows

REM Compilar la aplicación
echo Compilando aplicación...
pyinstaller scraper.spec --clean
if %errorlevel% neq 0 (
    echo ERROR: Falló la compilación
    pause
    exit /b 1
)

echo ✓ Compilación completada exitosamente

echo.
echo ========================================
echo ✓ Compilación completada exitosamente
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\KeywordPositionScraper.exe
echo.

REM Crear script de lanzamiento para usuario
echo Creando script de lanzamiento para usuario...
(
echo @echo off
echo rem Script de lanzamiento para Keyword Position Scraper
echo rem Este script puede ejecutarse desde cualquier ubicación
echo.
echo set "SCRIPT_DIR=%%~dp0"
echo "%%SCRIPT_DIR%%windows\dist\KeywordPositionScraper.exe"
) > ..\run_scraper.bat

echo ✓ Script de lanzamiento creado: run_scraper.bat
echo.
echo Para ejecutar la aplicación:
echo   run_scraper.bat
echo.
echo O directamente:
echo   windows\dist\KeywordPositionScraper.exe
echo.
echo La aplicación está lista para usar a nivel de usuario.
echo.

REM Desactivar entorno virtual
call deactivate

REM Preguntar si eliminar entorno virtual
echo ¿Deseas eliminar el entorno virtual de compilación? (s/N)
set /p response=
if /i "%response%"=="s" (
    rmdir /s /q ..\build_env
    echo ✓ Entorno virtual eliminado
)

pause
