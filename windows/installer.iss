; Script de instalación para Keyword Position Scraper
; Creado con Inno Setup Compiler

#define MyAppName "Keyword Position Scraper"
#define MyAppVersion "2.2.0"
#define MyAppPublisher "Tu Empresa"
#define MyAppURL "https://tuempresa.com"
#define MyAppExeName "KeywordPositionScraper.exe"

[Setup]
; NOTA: El valor de AppId identifica de forma única esta aplicación.
; No uses el mismo AppId en otro instalador.
; (Generar un nuevo AppId usando Tools > Generate GUID en el IDE de Inno Setup)
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Eliminar la siguiente línea para ejecutar en modo administrativo.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer
OutputBaseFilename=KeywordPositionScraper_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTA: No copiar todos los archivos desde la ubicación de la aplicación (ejemplo comentado)

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Función para verificar si .NET Framework está instalado (opcional)
function IsDotNetDetected(version: string; service: cardinal): boolean;
var
    key: string;
    install, release, serviceCount: cardinal;
    check45, success: boolean;
begin
    // .NET 4.5 y posteriores
    if version = 'v4.5' then
    begin
        Result := IsWin64 and
            (RegQueryDWordValue(HKLM, 'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full', 'Release', release) and
            (release >= 378389));
        exit;
    end;

    // Versiones anteriores
    key := 'SOFTWARE\Microsoft\NET Framework Setup\NDP\' + version;
    // Versiones de 64 bits
    if IsWin64 then
        Result := RegQueryDWordValue(HKLM64, key, 'Install', install) and
            (install = 1) and
            ((service = 0) or
            RegQueryDWordValue(HKLM64, key, 'Service', serviceCount) and
            (serviceCount >= service))
    else
        Result := RegQueryDWordValue(HKLM, key, 'Install', install) and
            (install = 1) and
            ((service = 0) or
            RegQueryDWordValue(HKLM, key, 'Service', serviceCount) and
            (serviceCount >= service));
end;

// Función para inicializar el instalador
function InitializeSetup(): Boolean;
begin
    // Verificar requisitos del sistema aquí si es necesario
    Result := True;
end;

// Función para mostrar página personalizada al final de la instalación
procedure CurStepChanged(CurStep: TSetupStep);
begin
    if CurStep = ssPostInstall then
    begin
        // Aquí puedes agregar acciones post-instalación
    end;
end;
