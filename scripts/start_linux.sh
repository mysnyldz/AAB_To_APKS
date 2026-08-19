#!/bin/bash
set -u

cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"

echo ""
echo "========================================"
echo "  Bundle Tool Suite - Linux Launcher"
echo "========================================"
echo ""

pause_exit() {
    echo ""
    read -r -p "Press Enter to exit..."
    exit "${1:-1}"
}

# 1) Check Python
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] python3 not found."
    echo ""
    echo "Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "Fedora:        sudo dnf install python3 python3-pip"
    echo "Arch:          sudo pacman -S python python-pip"
    pause_exit 1
fi
echo "[INFO] Python $(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])') found."

# 2) Check Java (required for bundletool)
if ! command -v java &>/dev/null; then
    echo "[WARNING] Java not found - bundletool won't work."
    echo "          Ubuntu/Debian: sudo apt install default-jre"
    echo "          Fedora:        sudo dnf install java-latest-openjdk"
    echo ""
fi

# 3) Virtual environment (created on first run)
VENV="$ROOT/.venv"
if [ ! -d "$VENV" ]; then
    echo "[INFO] First-time setup, this may take a few minutes..."
    python3 -m venv "$VENV" || { echo "[ERROR] Failed to create venv."; pause_exit 1; }
fi
source "$VENV/bin/activate"

# 4) Dependencies
if ! python -c "import PySide6" &>/dev/null; then
    echo "[INFO] Installing dependencies (PySide6 ~100 MB, please wait)..."
    python -m pip install --upgrade pip --quiet
    python -m pip install -r "$ROOT/requirements.txt" || {
        echo "[ERROR] Failed to install dependencies."
        pause_exit 1
    }
    echo "[INFO] Installation complete."
fi

# 5) Run
echo "[INFO] Starting application..."
python "$ROOT/run.py"
STATUS=$?
[ $STATUS -ne 0 ] && { echo ""; echo "[ERROR] Application exited with code $STATUS."; pause_exit $STATUS; }
