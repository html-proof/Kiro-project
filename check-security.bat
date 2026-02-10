@echo off
REM Security Check Script - Verify no secrets in Git

echo.
echo 🔒 Security Check
echo =================
echo.

echo Checking for sensitive files in Git...
echo.

REM Check if .env is tracked
git ls-files | findstr /C:".env" | findstr /V ".env.example" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ❌ DANGER: .env file is tracked by Git!
    echo    Run: git rm --cached .env
    echo.
) else (
    echo ✅ .env file is NOT in Git
)

REM Check for Firebase JSON files
git ls-files | findstr "firebase.*\.json" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ❌ DANGER: Firebase JSON file is tracked by Git!
    echo    Run: git rm --cached app/*firebase*.json
    echo.
) else (
    echo ✅ No Firebase JSON files in Git
)

REM Check .gitignore exists
if exist .gitignore (
    echo ✅ .gitignore file exists
) else (
    echo ❌ WARNING: .gitignore file missing!
)

REM Check if .gitignore has .env
findstr /C:".env" .gitignore >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ .env is in .gitignore
) else (
    echo ❌ WARNING: .env not in .gitignore!
)

REM Check if .gitignore has firebase pattern
findstr /C:"firebase" .gitignore >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Firebase files are in .gitignore
) else (
    echo ❌ WARNING: Firebase pattern not in .gitignore!
)

echo.
echo 📋 Files in Git:
git ls-files | findstr /C:".env" /C:"firebase" /C:"secret" /C:"key"

echo.
echo 🔍 Untracked files:
git status --short | findstr "^\?\?"

echo.
echo ✅ Security check complete!
echo.

pause
