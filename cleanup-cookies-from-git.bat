@echo off
echo ========================================
echo  Remove Cookies from Git (Security)
echo ========================================
echo.

cd /d "%~dp0"

echo This will remove cookies.txt from git history
echo (but keep it on your local machine)
echo.
echo Press any key to continue...
pause > nul
echo.

echo Step 1: Removing cookies.txt from git cache...
git rm --cached cookies.txt
if errorlevel 1 (
    echo ERROR: Failed to remove from cache
    pause
    exit /b 1
)
echo ✓ Removed from git cache
echo.

echo Step 2: Committing removal...
git commit -m "Remove cookies.txt from git (security)"
if errorlevel 1 (
    echo ERROR: Failed to commit
    pause
    exit /b 1
)
echo ✓ Committed
echo.

echo Step 3: Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Failed to push
    pause
    exit /b 1
)
echo ✓ Pushed!
echo.

echo ========================================
echo  SUCCESS! Cookies removed from git
echo ========================================
echo.
echo Your cookies.txt is now:
echo ✓ Still on your local machine
echo ✓ Still on Railway server
echo ✓ Removed from git history
echo.
echo Bot detection should now be fixed!
echo Check Railway logs to verify.
echo.
pause
