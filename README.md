# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A cross-platform GUI application for converting AAB (Android App Bundle) files to APKs format using bundletool, and signing APKs for distribution on platforms like Xiaomi GetApps.

**Languages:** [English](README.md) | [Türkçe](docs/README_TR.md) | [Deutsch](docs/README_DE.md) | [Español](docs/README_ES.md) | [Français](docs/README_FR.md) | [日本語](docs/README_JA.md) | [简体中文](docs/README_ZH-CN.md) | [Русский](docs/README_RU.md)

---

## Features

### AAB to APKs Conversion
- Convert AAB files to APKs format using Google's bundletool
- Keystore-based signing support
- Password input via text field or TXT file
- Real-time output logging

### APK Signing & Renaming
- Sign APK files with custom keystore
- Automatic renaming to `com.xiaomi.getapps.signature.verification.apk`
- Compatible with Xiaomi GetApps submission requirements

### General
- Multi-language UI (8 languages: EN, TR, DE, ES, FR, JA, ZH-CN, RU)
- Tabbed interface
- File browser dialogs
- Progress indicators
- Cross-platform (Windows, macOS, Linux)
- Automatic Android SDK detection
- Bundled bundletool JAR support

---

## Requirements

### System
- **Python 3.10+** (for running from source)
- **Java Runtime Environment (JRE)** (required by bundletool)
- **PySide6** (Qt6 GUI framework) — auto-installed by build scripts, or install manually: `pip install PySide6`

### External Tools
- **bundletool** - Google's official tool for AAB conversion
  - Download: https://github.com/google/bundletool/releases
  - Place `bundletool-all-x.x.x.jar` in the `tools/` folder or add to PATH
- **Android SDK build-tools** - Required for APK signing
  - Included with Android Studio
  - Automatically detected on all platforms

---

## Installation

### Option A: Quick Start (Recommended)

Double-click the launcher for your platform (in the `scripts/` folder):

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

The launcher will automatically:
1. Create a virtual environment (`.venv`) on first run
2. Install dependencies (PySide6 ~100 MB)
3. Start the application

**macOS Gatekeeper Note:** If you see "cannot be opened because the developer cannot be verified", right-click the file and select "Open". This is a macOS security feature for downloaded files.

**First Run:** The initial setup may take a few minutes as dependencies are downloaded. Subsequent runs start immediately.

### Option B: Run from Source

```bash
git clone <repo-url>
cd AAB-To-APKs

# Run the application
python run.py
```

### Option C: Standalone Executable

#### Windows:
```bash
scripts/build_windows.bat
# Output: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# Output: dist/BundleToolSuite
```

> **Note:** Building executables requires [PyInstaller](https://pyinstaller.org/):
> ```bash
> pip install pyinstaller
> ```

### Clean / fresh install

To remove `.venv`, `dist`, and `build` (source code is kept):

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

These folders are listed in `.gitignore`, so they are not pushed to GitHub.

---

## Usage

### AAB to APKs

1. Select your `.aab` file
2. Set the output `.apks` file path
3. Provide keystore file, password, key alias, and key password
4. Click **Convert to APKs**

### APK Signing

1. Select your source `.apk` file
2. Set the output directory
3. Provide keystore file, password, key alias, and key password
4. Click **Sign & Rename APK**
5. Output: `com.xiaomi.getapps.signature.verification.apk`

### Password from TXT File

Both tabs support reading passwords from a TXT file instead of typing them directly. Check the **"Read from TXT"** option and browse to your password file.

---

## Project Structure

```
AAB-To-APKs/
├── main_window.py           # Main PySide6 GUI application
├── theme.py                 # Design tokens and QSS stylesheet
├── errors.py                # Error classification and user-friendly messages
├── run.py                   # Application launcher
├── requirements.txt         # Python dependencies (PySide6)
├── README.md                # This file (English)
├── .gitignore
├── i18n/                    # Internationalization
│   ├── tr.json              # Turkish
│   └── en.json              # English
├── assets/                  # Icons and fonts
│   ├── icon.png             # Application icon
│   └── icons/               # SVG icons
├── docs/                    # Documentation
│   ├── BUILD.md             # Build instructions
│   ├── README_TR.md         # Turkish
│   ├── README_DE.md         # German
│   ├── README_ES.md         # Spanish
│   ├── README_FR.md         # French
│   ├── README_JA.md         # Japanese
│   ├── README_ZH-CN.md      # Chinese (Simplified)
│   └── README_RU.md         # Russian
├── scripts/                 # Build & launcher scripts
│   ├── build_simple.sh      # Build script (macOS/Linux)
│   ├── build_macos.sh       # macOS .app build script
│   ├── build_windows.bat    # Windows .exe build script
│   ├── start_windows.bat    # Windows launcher (double-click)
│   ├── start_macos.command  # macOS launcher (double-click)
│   ├── start_linux.sh       # Linux launcher (double-click)
│   ├── clean_windows.bat    # Remove .venv / dist / build (Windows)
│   └── clean.sh             # Remove .venv / dist / build (macOS/Linux)
├── tools/                   # External tools
│   └── bundletool-all-*.jar # Place bundletool JAR here
└── examples/                # Example CLI commands
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## Troubleshooting

### bundletool not found
- Ensure bundletool is in PATH or placed in the `tools/` folder
- Verify Java is installed: `java -version`
- Test manually: `bundletool` or `java -jar tools/bundletool-all-x.x.x.jar`

### apksigner not found
- Install Android Studio or Android SDK
- Ensure build-tools are installed
- The app auto-detects SDK paths on Windows, macOS, and Linux

### Keystore errors
- Verify keystore file format (`.keystore` or `.jks`)
- Double-check password and alias
- Ensure keystore file is not corrupted

### AAB file errors
- Ensure the AAB file is valid and not corrupted
- Avoid special characters or spaces in file paths

---

## Technical Details

The application executes the following commands:

**AAB to APKs:**
```bash
bundletool build-apks \
  --bundle=/path/to/app.aab \
  --output=/path/to/app.apks \
  --ks=/path/to/keystore.keystore \
  --ks-pass=pass:PASSWORD \
  --ks-key-alias=ALIAS \
  --key-pass=pass:PASSWORD
```

**APK Signing:**
```bash
apksigner sign \
  --ks /path/to/keystore.keystore \
  --ks-pass pass:PASSWORD \
  --ks-key-alias ALIAS \
  --key-pass pass:PASSWORD \
  --out singer.apk \
  source.apk
```

---

## Platform Support

| Platform | Support |
|----------|---------|
| Windows  | Full    |
| macOS    | Full    |
| Linux    | Full    |

---

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Bug reports and suggestions are welcome. Please open an issue on GitHub.
