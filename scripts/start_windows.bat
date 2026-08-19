@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Bundle Tool Suite

cd /d "%~dp0\.."
set "ROOT=%CD%"

echo.
echo ========================================
echo   Bundle Tool Suite - Windows Launcher
echo ========================================
echo.

REM 1) Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYVER=%%i
echo [INFO] Python %PYVER% found.

REM 2) Check Java (required for bundletool)
where java >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Java not found - bundletool won't work.
    echo           Download from: https://adoptium.net/
    echo.
)

REM 3) Virtual environment (created on first run)
set "VENV=%ROOT%\.venv"
if not exist "%VENV%" (
    echo [INFO] First-time setup, this may take a few minutes...
    python -m venv "%VENV%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
)
call "%VENV%\Scripts\activate.bat"

REM 4) Dependencies
python -c "import PySide6" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies ^(PySide6 ~100 MB, please wait^)...
    python -m pip install --upgrade pip --quiet
    python -m pip install -r "%ROOT%\requirements.txt"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo [INFO] Installation complete.
)

REM 5) Run
echo [INFO] Starting application...
python "%ROOT%\run.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with code %errorlevel%.
    pause
)
