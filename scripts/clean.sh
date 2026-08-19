#!/bin/bash
set -u

cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"

echo ""
echo "========================================"
echo "  Bundle Tool Suite - Clean"
echo "========================================"
echo ""
echo "This removes local setup and build files:"
echo ""
echo "  .venv          virtual environment"
echo "  dist           built executable"
echo "  build          PyInstaller work files"
echo "  *.spec         PyInstaller spec"
echo "  __pycache__    Python cache"
echo ""
echo "Source code is not touched."
echo "After this, the start/build scripts will do a fresh install."
echo ""
read -r -p "Continue? [y/N] " CONFIRM
case "$CONFIRM" in
    y|Y) ;;
    *) echo "Cancelled."; exit 0 ;;
esac
echo ""

FAILED=0

remove_dir() {
    local name="$1"
    if [ -d "$ROOT/$name" ]; then
        echo "[INFO] Removing $name..."
        rm -rf "$ROOT/$name"
        if [ -d "$ROOT/$name" ]; then
            echo "[WARN] Could not remove $name — close Python/IDE and retry."
            FAILED=1
        else
            echo "       Removed $name"
        fi
    fi
}

remove_dir ".venv"
remove_dir "venv"
remove_dir "env"
remove_dir "build"
remove_dir "dist"

rm -f "$ROOT"/*.spec "$ROOT"/warn-*.txt
rm -f "$ROOT/BundleToolSuite" "$ROOT/Bundle Tool Suite.exe"
rm -rf "$ROOT/Bundle Tool Suite.app" "$ROOT/BundleToolSuite.app"

find "$ROOT" -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null

echo ""
if [ "$FAILED" -eq 1 ]; then
    echo "[WARN] Some folders could not be deleted."
    echo "       Close the app and retry."
    exit 1
fi

echo "[SUCCESS] Clean complete. Ready for a fresh setup."
