# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

Eine plattformübergreifende GUI-Anwendung zum Konvertieren von AAB-Dateien (Android App Bundle) in das APKs-Format mit bundletool und zum Signieren von APKs für die Verteilung auf Plattformen wie Xiaomi GetApps.

**Sprachen:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## Funktionen

### AAB zu APKs Konvertierung
- Konvertierung von AAB-Dateien in das APKs-Format mit Googles bundletool
- Keystore-basierte Signierung
- Passworteingabe über Textfeld oder TXT-Datei
- Echtzeit-Ausgabeprotokollierung

### APK-Signierung und Umbenennung
- Signierung von APK-Dateien mit benutzerdefiniertem Keystore
- Automatische Umbenennung in `com.xiaomi.getapps.signature.verification.apk`
- Kompatibel mit Xiaomi GetApps-Einreichungsanforderungen

### Allgemein
- Mehrsprachige Benutzeroberfläche (8 Sprachen: EN, TR, DE, ES, FR, JA, ZH-CN, RU)
- Registerkarten-basierte Oberfläche
- Dateiauswahldialoge
- Fortschrittsanzeigen
- Plattformübergreifend (Windows, macOS, Linux)
- Automatische Android SDK-Erkennung
- Integrierte bundletool-JAR-Unterstützung

---

## Anforderungen

### System
- **Python 3.10+** (zum Ausführen aus dem Quellcode)
- **Java Runtime Environment (JRE)** (von bundletool benötigt)
- **PySide6** (Qt6 GUI-Framework) — wird von Build-Scripten automatisch installiert, oder manuell: `pip install PySide6`

### Externe Tools
- **bundletool** - Googles offizielles Tool zur AAB-Konvertierung
  - Download: https://github.com/google/bundletool/releases
  - `bundletool-all-x.x.x.jar` in den `tools/`-Ordner legen oder zum PATH hinzufügen
- **Android SDK build-tools** - Erforderlich für APK-Signierung
  - In Android Studio enthalten
  - Wird auf allen Plattformen automatisch erkannt

---

## Installation

### Option A: Schnellstart (Empfohlen)

Doppelklicken Sie auf den Launcher für Ihre Plattform (im Ordner `scripts/`):

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

Der Launcher:
1. erstellt beim ersten Start eine virtuelle Umgebung (`.venv`)
2. installiert Abhängigkeiten (PySide6 ~100 MB)
3. startet die Anwendung

### Option B: Aus dem Quellcode ausführen

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### Option C: Standalone Executable

#### Windows:
```bash
scripts/build_windows.bat
# Ausgabe: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# Ausgabe: dist/BundleToolSuite
```

> **Hinweis:** Zum Erstellen von Executables ist [PyInstaller](https://pyinstaller.org/) erforderlich:
> ```bash
> pip install pyinstaller
> ```

### Clean / Neuinstallation

Zum Löschen von `.venv`, `dist` und `build` (Quellcode bleibt erhalten):

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

Diese Ordner stehen in `.gitignore` und werden nicht zu GitHub hochgeladen.

---

## Verwendung

### AAB zu APKs

1. `.aab`-Datei auswählen
2. Ausgabe-`.apks`-Dateipfad festlegen
3. Keystore-Datei, Passwort, Schlüssel-Alias und Schlüssel-Passwort eingeben
4. Auf **In APKs konvertieren** klicken

### APK-Signierung

1. Quell-`.apk`-Datei auswählen
2. Ausgabeverzeichnis festlegen
3. Keystore-Datei, Passwort, Schlüssel-Alias und Schlüssel-Passwort eingeben
4. Auf **APK signieren & umbenennen** klicken
5. Ausgabe: `com.xiaomi.getapps.signature.verification.apk`

### Passwort aus TXT-Datei

Beide Registerkarten unterstützen das Lesen von Passwörtern aus einer TXT-Datei. Aktivieren Sie die Option **"Aus TXT lesen"** und wählen Sie Ihre Passwortdatei aus.

---

## Projektstruktur

```
AAB-To-APKs/
├── main_window.py           # Haupt-PySide6-GUI
├── theme.py                 # Design-Tokens und QSS
├── errors.py                # Fehlerklassifizierung und Meldungen
├── run.py                   # Anwendungsstarter
├── requirements.txt         # Python-Abhängigkeiten (PySide6)
├── README.md                # Englisch
├── .gitignore
├── i18n/                    # Übersetzungen
│   ├── tr.json              # Türkisch
│   └── en.json              # Englisch
├── assets/                  # Icons und Schriftarten
│   ├── icon.png             # Anwendungssymbol
│   └── icons/               # SVG-Icons
├── docs/                    # Dokumentation
│   ├── BUILD.md             # Build-Anweisungen
│   ├── README_TR.md         # Türkisch
│   ├── README_DE.md         # Diese Datei (Deutsch)
│   ├── README_ES.md         # Spanisch
│   ├── README_FR.md         # Französisch
│   ├── README_JA.md         # Japanisch
│   ├── README_ZH-CN.md      # Chinesisch (vereinfacht)
│   └── README_RU.md         # Russisch
├── scripts/                 # Build- und Launcher-Scripts
│   ├── build_simple.sh      # Build (macOS/Linux)
│   ├── build_macos.sh       # macOS-.app-Build
│   ├── build_windows.bat    # Windows-.exe-Build
│   ├── start_windows.bat    # Windows-Launcher
│   ├── start_macos.command  # macOS-Launcher
│   ├── start_linux.sh       # Linux-Launcher
│   ├── clean_windows.bat    # .venv / dist / build löschen (Windows)
│   └── clean.sh             # .venv / dist / build löschen (macOS/Linux)
├── tools/                   # Externe Tools
│   └── bundletool-all-*.jar # bundletool-JAR hier ablegen
└── examples/                # Beispiel-CLI-Befehle
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## Fehlerbehebung

### bundletool nicht gefunden
- Sicherstellen, dass bundletool im PATH oder im `tools/`-Ordner ist
- Java-Installation überprüfen: `java -version`
- Manuell testen: `bundletool` oder `java -jar tools/bundletool-all-x.x.x.jar`

### apksigner nicht gefunden
- Android Studio oder Android SDK installieren
- Sicherstellen, dass build-tools installiert sind
- Die App erkennt SDK-Pfade auf Windows, macOS und Linux automatisch

### Keystore-Fehler
- Keystore-Dateiformat überprüfen (`.keystore` oder `.jks`)
- Passwort und Alias doppelt prüfen
- Sicherstellen, dass die Keystore-Datei nicht beschädigt ist

### AAB-Dateifehler
- Sicherstellen, dass die AAB-Datei gültig und nicht beschädigt ist
- Sonderzeichen oder Leerzeichen in Dateipfaden vermeiden

---

## Plattformunterstützung

| Plattform | Unterstützung |
|-----------|---------------|
| Windows   | Vollständig   |
| macOS     | Vollständig   |
| Linux     | Vollständig   |

---

## Lizenz

Dieses Projekt wurde zu Bildungszwecken entwickelt.

## Beitrag leisten

Fehlerberichte und Vorschläge sind willkommen. Bitte öffnen Sie ein Issue auf GitHub.
