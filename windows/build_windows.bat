@echo off
echo ========================================
echo  Keyword Position Scraper - Windows Build
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Cambiar al directorio padre (donde está requirements.txt)
cd /d "%~dp0\.."

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación de dependencias
    pause
    exit /b 1
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
pyinstaller scraper.spec
if %errorlevel% neq 0 (
    echo ERROR: Falló la compilación
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ Compilación completada exitosamente
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\KeywordPositionScraper.exe
echo.
pause