; Setup classico Windows per Cantiere Navale Pro.
; Compilare con Inno Setup 6:  ISCC installer.iss
; Versione opzionale da riga di comando:  ISCC /DAPP_VERSION=2.1 installer.iss

#ifndef APP_VERSION
#define APP_VERSION "2.0"
#endif

[Setup]
AppId={{9C6F1E52-8D3A-4B77-9F2E-6A31D5C70A12}
AppName=Cantiere Navale Pro
AppVersion={#APP_VERSION}
AppPublisher=Cantiere Navale Pro
DefaultDirName={autopf}\Cantiere Navale Pro
DefaultGroupName=Cantiere Navale Pro
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=CantiereNavalePro-Setup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\CantiereNavalePro.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Files]
Source: "dist\CantiereNavalePro\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Crea un collegamento sul desktop"; GroupDescription: "Collegamenti:"

[Icons]
Name: "{group}\Cantiere Navale Pro"; Filename: "{app}\CantiereNavalePro.exe"
Name: "{group}\Disinstalla Cantiere Navale Pro"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Cantiere Navale Pro"; Filename: "{app}\CantiereNavalePro.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CantiereNavalePro.exe"; Description: "Avvia Cantiere Navale Pro"; Flags: nowait postinstall skipifsilent
