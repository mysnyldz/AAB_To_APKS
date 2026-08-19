# Bundle Tool Suite - Build Instructions

This file contains instructions for building Bundle Tool Suite into standalone executable files.

## Quick Start

### macOS / Linux:
```bash
./build_simple.sh
```

### Windows:
```bash
build_windows.bat
```

## Build Outputs

After the build process completes, you will find the following in the `dist/` folder:

### macOS:
- `BundleToolSuite.app` - Double-click to open .app bundle
- `BundleToolSuite` - Terminal-runnable executable

### Windows:
- `Bundle Tool Suite.exe` - Double-click to open .exe

## Build Scripts

### 1. `build_simple.sh` (Recommended - macOS/Linux)
- Simple build without icon
- Creates executable
- Fast and reliable

### 2. `build_macos.sh` (Advanced macOS)
- Icon support (requires `app_icon.icns`)
- Creates .app bundle only
- macOS optimizations

### 3. `build_windows.bat` (Windows)
- Icon support (requires `app_icon.ico`)
- Creates .exe file
- Windows optimizations

## Requirements

### Python Packages:
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate        # macOS/Linux
# or
venv\Scripts\activate.bat       # Windows

# Install PyInstaller
pip install pyinstaller
```

### System Requirements:
- Python 3.6+
- PyInstaller
- Sufficient disk space (~50MB for build)

## Build Process

1. **Preparation:**
   - Virtual environment active
   - PyInstaller installed
   - Old build files cleaned

2. **Compilation:**
   - Python code compiled to bytecode
   - All dependencies packaged
   - Standalone executable created

3. **Output:**
   - Single file (onefile mode)
   - GUI mode (windowed)
   - Platform native format

## File Sizes

- **macOS executable**: ~9.5MB
- **Windows .exe**: ~15-20MB (estimated)

## Troubleshooting

### Tkinter Error:
```bash
# macOS
brew install python-tk

# Linux (Ubuntu/Debian)
sudo apt-get install python3-tk
```

### PyInstaller Error:
```bash
pip uninstall pyinstaller
pip install pyinstaller
```

### Build Failed:
```bash
# Clean and retry
./scripts/clean.sh          # macOS / Linux
scripts\clean_windows.bat   # Windows
./scripts/build_simple.sh
```

## Clean / fresh install

To delete `.venv`, `dist`, `build`, and Python cache (source code is kept):

```bash
# Windows
scripts\clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

These folders are listed in `.gitignore`, so they are not pushed to GitHub. After cleaning, run the start or build script again for a fresh setup.

## Distribution

### macOS:
1. Send `BundleToolSuite.app` to the user
2. User can double-click to open
3. Or copy to Applications folder

### Windows:
1. Send `Bundle Tool Suite.exe` to the user
2. User can double-click to open
3. Can be copied anywhere and run

## Notes

- Executable files may be large (includes entire Python runtime)
- First launch may be slightly slow (filesystem check)
- `bundletool` and `apksigner` commands must be in system PATH or placed in the `Bundletool/` folder
- Android SDK build-tools required for APK signing

## CI/CD

GitHub Actions or similar CI/CD pipeline can be added for automated builds in future updates.
