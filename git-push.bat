@echo off
REM Git Push Script for Windows

echo.
echo 🚀 Git Push to GitHub
echo =====================
echo.

REM Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git is not installed!
    echo.
    echo Install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

REM Check if .env exists and warn
if exist .env (
    echo ⚠️  WARNING: .env file detected
    echo    This file contains secrets and should NOT be pushed to GitHub
    echo    It is protected by .gitignore
    echo.
)

REM Check if already initialized
if not exist .git (
    echo 📦 Initializing Git repository...
    git init
    echo.
)

REM Check current status
echo 📋 Current Git status:
git status --short
echo.

REM Ask for confirmation
set /p CONFIRM="Continue with push? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ Push cancelled
    pause
    exit /b 1
)

echo.
echo 📝 Adding files...
git add .

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to add files
    pause
    exit /b 1
)

echo ✅ Files added
echo.

REM Ask for commit message
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Initial commit: Complete Musicly Backend
)

echo.
echo 💾 Committing changes...
git commit -m "%COMMIT_MSG%"

if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Nothing to commit or commit failed
    echo.
)

echo.
echo 🌿 Setting main branch...
git branch -M main

echo.
echo 🔗 Checking remote...
git remote -v | findstr origin >nul 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo Adding remote origin...
    git remote add origin https://github.com/html-proof/Kiro-project.git
) else (
    echo Remote origin already exists
)

echo.
echo 🚀 Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🔗 View your repository:
    echo    https://github.com/html-proof/Kiro-project
    echo.
    echo 📋 Next steps:
    echo    1. Verify files on GitHub
    echo    2. Check .env is NOT visible
    echo    3. Deploy to Railway (see DEPLOYMENT.md)
    echo.
) else (
    echo.
    echo ❌ Push failed!
    echo.
    echo Common solutions:
    echo    1. Check internet connection
    echo    2. Verify GitHub credentials
    echo    3. Try: git pull origin main --rebase
    echo    4. Then: git push origin main
    echo.
)

pause
