#!/bin/bash
set -u

cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"

echo ""
echo "========================================"
echo "  Bundle Tool Suite - macOS Build"
echo "========================================"
echo ""

# Virtual environment
VENV="$ROOT/.venv"
if [ ! -d "$VENV" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv "$VENV" || { echo "[ERROR] Failed to create venv."; exit 1; }
fi
source "$VENV/bin/activate"

echo "[1/4] Checking PyInstaller..."
if ! command -v pyinstaller &> /dev/null; then
    echo "       Installing PyInstaller..."
    python -m pip install pyinstaller --quiet || {
        echo "[ERROR] Failed to install PyInstaller."
        exit 1
    }
    echo "       PyInstaller installed."
else
    echo "       PyInstaller found."
fi

echo "[2/4] Checking PySide6..."
python -c "import PySide6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "       Installing PySide6..."
    python -m pip install PySide6 --quiet || {
        echo "[ERROR] Failed to install PySide6."
        exit 1
    }
    echo "       PySide6 installed."
else
    echo "       PySide6 found."
fi

echo "[3/4] Cleaning old build artifacts..."
rm -rf build/
rm -rf dist/
rm -f *.spec

echo "[4/4] Building .app..."
pyinstaller --windowed --onedir \
    --name "BundleToolSuite" \
    --osx-bundle-identifier com.bundletool.suite \
    --add-data "i18n:i18n" \
    --add-data "assets:assets" \
    --add-data "examples:examples" \
    run.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCESS] Build complete!"
    echo ""
    echo "  Output: dist/BundleToolSuite.app"
    echo ""
    echo "  To create DMG:"
    echo "  hdiutil create -volname \"Bundle Tool Suite\" -srcfolder dist/BundleToolSuite.app -ov -format UDZO BundleToolSuite.dmg"
else
    echo ""
    echo "[ERROR] Build failed!"
    exit 1
fi
