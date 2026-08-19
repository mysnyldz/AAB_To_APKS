@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0\.."
set "ROOT=%CD%"
set "VENV=%ROOT%\.venv"
set "PY=%VENV%\Scripts\python.exe"

echo.
echo ========================================
echo   Bundle Tool Suite - Windows Build
echo ========================================
echo.

REM Virtual environment
if not exist "%PY%" (
    echo [INFO] Creating virtual environment...
    python -m venv "%VENV%"
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
)

echo [1/4] Checking PyInstaller...
"%PY%" -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo        Installing PyInstaller...
    "%PY%" -m pip install --upgrade pip
    "%PY%" -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller.
        pause
        exit /b 1
    )
    echo        PyInstaller installed.
) else (
    echo        PyInstaller found.
)

echo [2/4] Checking PySide6...
"%PY%" -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo        Installing PySide6...
    "%PY%" -m pip install PySide6
    if errorlevel 1 (
        echo [ERROR] Failed to install PySide6.
        pause
        exit /b 1
    )
    echo        PySide6 installed.
) else (
    echo        PySide6 found.
)

echo [3/4] Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del /q *.spec 2>nul

REM Create assets folder if missing
if not exist assets mkdir assets

echo [4/4] Building executable...
"%PY%" -m PyInstaller --onefile ^
    --windowed ^
    --name "BundleToolSuite" ^
    --add-data "i18n;i18n" ^
    --add-data "assets;assets" ^
    --add-data "examples;examples" ^
    run.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build complete!
echo.
echo   Output: dist\BundleToolSuite.exe

pause
