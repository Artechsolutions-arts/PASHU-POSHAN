@echo off
setlocal
echo ==================================================
echo    FORAGE - WEB DASHBOARD (LOCAL SERVER)
echo ==================================================
echo.

cd /d "%~dp0"

:: Check for virtual environment
if exist venv\Scripts\python.exe (
    echo [INFO] Using Virtual Environment...
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    echo [INFO] Using System Python...
    set PYTHON_CMD=python
)

:: Install dependencies if needed (quick check)
%PYTHON_CMD% -c "import uvicorn, fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required server dependencies...
    %PYTHON_CMD% -m pip install fastapi uvicorn
)

echo.
echo [INFO] Starting Local Server...
echo [SUCCESS] Dashboard is running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

%PYTHON_CMD% -m uvicorn api.index:app --reload --port 8000 --host 0.0.0.0

pause
