@echo off
echo ===========================================
echo    FORAGE - GITHUB SYNC UTILITY
echo ===========================================
echo.

:: Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please download and install Git from: https://git-scm.com/download/win
    echo After installing, restart your computer and run this script again.
    pause
    exit /b
)

echo [INFO] Initializing Repository...
git init

echo [INFO] Adding files...
git add .

echo [INFO] Committing files...
git commit -m "Initial Release: Forage Analytics Platform (v1.0)"

echo [INFO] Rename branch to main...
git branch -M main

echo [INFO] Setting remote origin...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/Artechsolutions-arts/PASHU-POSHAN

echo [INFO] Pushing to GitHub...
git push -u origin main

echo.
echo ===========================================
echo [SUCCESS] Push complete!
echo ===========================================
pause
