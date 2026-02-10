@echo off
REM GitHub Push Script with Force Option

echo.
echo 🚀 Push to GitHub
echo ==================
echo.

echo Your repository: https://github.com/html-proof/Kiro-project
echo.

echo ⚠️  The remote has different history.
echo    You need to force push to overwrite it.
echo.

set /p CONFIRM="Force push to GitHub? This will overwrite remote. (y/n): "

if /i not "%CONFIRM%"=="y" (
    echo ❌ Push cancelled
    pause
    exit /b 1
)

echo.
echo 🚀 Force pushing to GitHub...
echo.

git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🔗 View your repository:
    echo    https://github.com/html-proof/Kiro-project
    echo.
    echo 🔒 IMPORTANT: Rotate your Firebase key!
    echo    1. Go to Firebase Console
    echo    2. Delete old service account key
    echo    3. Generate new key
    echo    4. Update .env file
    echo.
) else (
    echo.
    echo ❌ Push failed!
    echo.
    echo Possible issues:
    echo   - Authentication failed (use Personal Access Token)
    echo   - Network error
    echo   - GitHub still detecting secrets
    echo.
    echo See GITHUB_PUSH_FIX.md for solutions
    echo.
)

pause
