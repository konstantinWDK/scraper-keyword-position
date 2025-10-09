# Script PowerShell para habilitar soporte de rutas largas en Windows
# Este script resuelve el problema de "Windows Long Path Support" para pip

Write-Host "========================================" -ForegroundColor Green
Write-Host "Habilitando Soporte de Rutas Largas en Windows" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verificar si estamos ejecutando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "❌ ERROR: Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "   Por favor, ejecuta PowerShell como Administrador y vuelve a intentar" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Cómo ejecutar como Administrador:" -ForegroundColor Yellow
    Write-Host "   1. Busca 'PowerShell' en el menú Inicio" -ForegroundColor Yellow
    Write-Host "   2. Haz clic derecho y selecciona 'Ejecutar como administrador'" -ForegroundColor Yellow
    Write-Host "   3. Navega a esta carpeta y ejecuta: .\enable_long_paths.ps1" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ Ejecutando como Administrador" -ForegroundColor Green
Write-Host ""

# Habilitar soporte de rutas largas en el registro de Windows
Write-Host "Configurando soporte de rutas largas..." -ForegroundColor Yellow

try {
    # Verificar si ya está habilitado
    $currentValue = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -ErrorAction SilentlyContinue
    
    if ($currentValue -and $currentValue.LongPathsEnabled -eq 1) {
        Write-Host "✅ El soporte de rutas largas ya está habilitado" -ForegroundColor Green
    } else {
        # Habilitar soporte de rutas largas
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -Type DWord
        Write-Host "✅ Soporte de rutas largas habilitado en el registro" -ForegroundColor Green
    }
    
    # Configurar Python para usar rutas largas
    Write-Host "Configurando Python para usar rutas largas..." -ForegroundColor Yellow
    
    # Crear variable de entorno para pip
    [Environment]::SetEnvironmentVariable("PIP_USE_FEATURE", "2020-resolver", "Machine")
    Write-Host "✅ Variable de entorno PIP configurada" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎉 Configuración completada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Cambios realizados:" -ForegroundColor Cyan
    Write-Host "   • Soporte de rutas largas habilitado en Windows" -ForegroundColor Cyan
    Write-Host "   • Variable de entorno PIP configurada" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  Para que los cambios surtan efecto:" -ForegroundColor Yellow
    Write-Host "   1. Reinicia tu computadora" -ForegroundColor Yellow
    Write-Host "   2. Después del reinicio, ejecuta build_windows.bat nuevamente" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 El problema de 'No such file or directory' con rutas largas debería resolverse" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error durante la configuración: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Por favor, intenta ejecutar este script manualmente como Administrador" -ForegroundColor Yellow
}

Write-Host ""
pause
