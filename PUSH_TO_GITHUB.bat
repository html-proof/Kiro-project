@echo off
echo ========================================
echo Musicly Backend - Push to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo Git is installed: 
git --version
echo.

REM Check if this is already a git repository
if exist ".git" (
    echo [INFO] Git repository already exists
    echo.
) else (
    echo [1/6] Initializing Git repository...
    git init
    if errorlevel 1 (
        echo ERROR: Failed to initialize git repository
        pause
        exit /b 1
    )
    echo Git repository initialized!
    echo.
)

REM Check if remote exists
git remote -v | findstr "origin" >nul 2>&1
if errorlevel 1 (
    echo [2/6] Adding GitHub remote...
    echo.
    echo Enter your GitHub repository URL:
    echo Example: https://github.com/yourusername/musicly-backend.git
    set /p REPO_URL="Repository URL: "
    
    git remote add origin %REPO_URL%
    if errorlevel 1 (
        echo ERROR: Failed to add remote
        pause
        exit /b 1
    )
    echo Remote added successfully!
    echo.
) else (
    echo [2/6] Remote already configured:
    git remote -v
    echo.
)

REM Check for sensitive files
echo [3/6] Checking for sensitive files...
if exist ".env" (
    echo [OK] .env file found - will be ignored by .gitignore
)
if exist "app\music-app-f2e65-firebase-adminsdk-fbsvc-8787f0f5e5.json" (
    echo [OK] Firebase credentials found - will be ignored by .gitignore
)
echo.

REM Add all files
echo [4/6] Adding files to git...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo Files added successfully!
echo.

REM Show status
echo Current status:
git status --short
echo.

REM Commit
echo [5/6] Committing changes...
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=feat: Complete Musicly backend with advanced features

git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo WARNING: Nothing to commit or commit failed
    echo This might be okay if there are no changes
)
echo.

REM Push to GitHub
echo [6/6] Pushing to GitHub...
echo.
echo Choose branch name:
echo 1. main (recommended)
echo 2. master
echo 3. custom
set /p BRANCH_CHOICE="Enter choice (1-3): "

if "%BRANCH_CHOICE%"=="1" set BRANCH=main
if "%BRANCH_CHOICE%"=="2" set BRANCH=master
if "%BRANCH_CHOICE%"=="3" (
    set /p BRANCH="Enter branch name: "
)
if "%BRANCH%"=="" set BRANCH=main

echo.
echo Pushing to branch: %BRANCH%
git branch -M %BRANCH%
git push -u origin %BRANCH%

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Common issues:
    echo 1. Authentication failed - you may need to use a Personal Access Token
    echo 2. Repository doesn't exist - create it on GitHub first
    echo 3. Branch protection rules - check repository settings
    echo.
    echo To use Personal Access Token:
    echo 1. Go to GitHub Settings ^> Developer settings ^> Personal access tokens
    echo 2. Generate new token with 'repo' scope
    echo 3. Use token as password when prompted
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Code pushed to GitHub
echo ========================================
echo.
echo Repository: 
git remote get-url origin
echo Branch: %BRANCH%
echo.
echo Next steps:
echo 1. Visit your GitHub repository
echo 2. Set up GitHub Actions (optional)
echo 3. Deploy to Railway or other platform
echo.
pause
