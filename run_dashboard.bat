@echo off
setlocal
echo ==========================================
echo    FORAGE DASHBOARD LAUNCHER
echo ==========================================
echo.

cd /d "%~dp0"

:: Try matching venv
if exist venv\Scripts\python.exe (
    echo [INFO] Found virtual environment. Starting...
    venv\Scripts\python.exe -m streamlit run dashboard.py
) else (
    echo [WARN] Virtual environment not found.
    echo [INFO] Checking for Global Python...
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] Python found. Starting Streamlit...
        python -m streamlit run dashboard.py
    ) else (
        echo [ERROR] Python not found on this system!
        echo Please install Python and try again.
    )
)

echo.
echo Dashboard closed.
pause
