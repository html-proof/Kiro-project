@echo off
echo ========================================
echo  Upload Cookies to Railway
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking if cookies.txt exists...
if not exist "cookies.txt" (
    echo ERROR: cookies.txt not found!
    echo Please make sure cookies.txt is in the musicly-backend folder.
    pause
    exit /b 1
)
echo ✓ cookies.txt found!
echo.

echo Step 2: Adding cookies.txt to git (forced)...
git add -f cookies.txt
if errorlevel 1 (
    echo ERROR: Failed to add cookies.txt
    pause
    exit /b 1
)
echo ✓ Added to git
echo.

echo Step 3: Committing...
git commit -m "Add YouTube cookies (TEMPORARY - will remove after deploy)"
if errorlevel 1 (
    echo ERROR: Failed to commit
    pause
    exit /b 1
)
echo ✓ Committed
echo.

echo Step 4: Pushing to Railway...
git push origin main
if errorlevel 1 (
    echo ERROR: Failed to push
    pause
    exit /b 1
)
echo ✓ Pushed to Railway!
echo.

echo ========================================
echo  SUCCESS! Cookies uploaded to Railway
echo ========================================
echo.
echo Railway is now deploying with cookies.txt
echo This will take 2-3 minutes.
echo.
echo IMPORTANT: After Railway finishes deploying,
echo run the cleanup script to remove cookies from git!
echo.
echo Next step: Run "cleanup-cookies-from-git.bat"
echo.
pause
