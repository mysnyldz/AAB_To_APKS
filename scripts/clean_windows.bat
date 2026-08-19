@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

cd /d "%~dp0\.."
set "ROOT=%CD%"

echo.
echo ========================================
echo   Bundle Tool Suite - Clean
echo ========================================
echo.
echo This removes local setup and build files:
echo.
echo   .venv          virtual environment
echo   dist           built executable
echo   build          PyInstaller work files
echo   *.spec         PyInstaller spec
echo   __pycache__    Python cache
echo.
echo Source code is not touched.
echo After this, start_windows.bat / build_windows.bat
echo will do a fresh install.
echo.
set /p CONFIRM="Continue? (Y/N): "
if /i not "!CONFIRM!"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)
echo.

set "FAILED=0"

for %%D in (.venv venv env build dist) do (
    if exist "%ROOT%\%%D" (
        echo [INFO] Removing %%D...
        rmdir /s /q "%ROOT%\%%D" 2>nul
        if exist "%ROOT%\%%D" (
            echo [WARN] Could not remove %%D — close Python/IDE and retry.
            set "FAILED=1"
        ) else (
            echo        Removed %%D
        )
    )
)

del /q "%ROOT%\*.spec" 2>nul
del /q "%ROOT%\warn-*.txt" 2>nul
if exist "%ROOT%\Bundle Tool Suite.exe" del /q "%ROOT%\Bundle Tool Suite.exe" 2>nul
if exist "%ROOT%\BundleToolSuite.exe" del /q "%ROOT%\BundleToolSuite.exe" 2>nul

for /d /r "%ROOT%" %%P in (__pycache__) do (
    if exist "%%P" rmdir /s /q "%%P" 2>nul
)

echo.
if "!FAILED!"=="1" (
    echo [WARN] Some folders could not be deleted.
    echo        Close the app, terminal, and Cursor, then run this again.
) else (
    echo [SUCCESS] Clean complete. Ready for a fresh setup.
)
echo.
pause
