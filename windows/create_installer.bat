@echo off
echo ========================================
echo  Crear Instalador Profesional
echo ========================================
echo.

REM Verificar que el ejecutable existe
if not exist "dist\KeywordPositionScraper.exe" (
    echo ERROR: No se encontró el ejecutable compilado
    echo Ejecuta primero build_windows.bat para compilar la aplicación
    pause
    exit /b 1
)

echo ✓ Ejecutable encontrado: dist\KeywordPositionScraper.exe
echo.

REM Verificar si Inno Setup está instalado
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    echo INFO: Inno Setup no está instalado
    echo Creando instalador portátil alternativo...
    goto :CREATE_PORTABLE
)

echo ✓ Inno Setup encontrado
echo Compilando instalador profesional...

REM Crear directorio para el instalador
if not exist "installer" mkdir installer

REM Compilar el instalador
"%INNO_PATH%" installer.iss
if %errorlevel% neq 0 (
    echo ERROR: Falló la compilación del instalador con Inno Setup
    echo Creando instalador portátil alternativo...
    goto :CREATE_PORTABLE
)

echo.
echo ========================================
echo ✓ INSTALADOR PROFESIONAL CREADO
echo ========================================
echo.
echo El instalador se encuentra en: installer\KeywordPositionScraper_Setup.exe
echo.
echo Características del instalador:
echo - Instalación con interfaz gráfica moderna
echo - Creación de accesos directos en menú Inicio y escritorio
echo - Desinstalador completo
echo - Registro en Panel de Control
echo - Soporte multilingüe (Español/Inglés)
echo.
echo Para distribuir tu aplicación, comparte el archivo:
echo   installer\KeywordPositionScraper_Setup.exe
echo.
goto :END

:CREATE_PORTABLE
echo.
echo ========================================
echo  CREANDO INSTALADOR PORTÁTIL
echo ========================================
echo.

REM Crear directorio para el instalador portátil
if exist "portable_installer" rmdir /s /q "portable_installer"
mkdir "portable_installer"

REM Copiar archivos necesarios
echo Copiando archivos de la aplicación...
xcopy "dist\KeywordPositionScraper.exe" "portable_installer\" /Y /Q
xcopy "..\config\*" "portable_installer\config\" /Y /Q /S
xcopy "..\data\*" "portable_installer\data\" /Y /Q /S
xcopy "..\src\*" "portable_installer\src\" /Y /Q /S

REM Crear script de lanzamiento
echo Creando script de lanzamiento...
(
echo @echo off
echo.
echo ========================================
echo  Keyword Position Scraper - Versión Portátil
echo ========================================
echo.
echo Iniciando aplicación...
echo.
echo NOTA: Esta es una versión portátil que no requiere instalación.
echo       Puedes copiar esta carpeta a cualquier ubicación.
echo.
timeout /t 2 /nobreak >nul
echo.
start "" "KeywordPositionScraper.exe"
) > "portable_installer\Run_Scraper.bat"

REM Crear archivo README
(
echo KEYWORD POSITION SCRAPER - VERSIÓN PORTÁTIL
echo ============================================
echo.
echo INSTRUCCIONES DE USO:
echo.
echo 1. Para ejecutar la aplicación:
echo    - Doble clic en "Run_Scraper.bat" O
echo    - Doble clic en "KeywordPositionScraper.exe"
echo.
echo 2. Características:
echo    - No requiere instalación
echo    - Totalmente portátil
echo    - Puedes copiar la carpeta a cualquier ubicación
echo    - No modifica el registro de Windows
echo.
echo 3. Requisitos del sistema:
echo    - Windows 10/11 (64-bit)
echo    - No se requieren permisos de administrador
echo.
echo 4. Para desinstalar:
echo    - Simplemente elimina la carpeta completa
echo.
echo ============================================
echo ¡Disfruta usando Keyword Position Scraper!
echo ============================================
) > "portable_installer\README.txt"

echo ✓ Instalador portátil creado exitosamente
echo.
echo ========================================
echo ✓ INSTALADOR PORTÁTIL CREADO
echo ========================================
echo.
echo El instalador portátil se encuentra en: portable_installer\
echo.
echo Para distribuir tu aplicación, comparte la carpeta completa:
echo   portable_installer\
echo.
echo O puedes crear un archivo ZIP:
echo   portable_installer.zip
echo.
echo Instrucciones para el usuario final:
echo - Descomprimir la carpeta en cualquier ubicación
echo - Ejecutar "Run_Scraper.bat" o "KeywordPositionScraper.exe"
echo.

:END
echo.
echo Resumen de opciones de distribución:
echo.
echo 1. INSTALADOR PROFESIONAL (Recomendado):
echo    - installer\KeywordPositionScraper_Setup.exe
echo    - Requiere Inno Setup instalado
echo.
echo 2. VERSIÓN PORTÁTIL:
echo    - portable_installer\ (carpeta completa)
echo    - No requiere instalación
echo.
echo 3. EJECUTABLE DIRECTO:
echo    - windows\dist\KeywordPositionScraper.exe
echo    - Para usuarios técnicos
echo.
pause
