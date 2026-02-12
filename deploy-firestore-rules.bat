@echo off
echo ========================================
echo   Firestore Rules Deployment Script
echo ========================================
echo.

echo Checking if Firebase CLI is installed...
where firebase >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Firebase CLI not found!
    echo.
    echo Please install it first:
    echo   npm install -g firebase-tools
    echo.
    pause
    exit /b 1
)

echo [OK] Firebase CLI found
echo.

echo Logging in to Firebase...
call firebase login
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Login failed
    pause
    exit /b 1
)

echo.
echo Deploying Firestore rules...
call firebase deploy --only firestore:rules
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS! Rules deployed
echo ========================================
echo.
echo Next steps:
echo 1. Test the Flutter app
echo 2. Check logs for PERMISSION_DENIED errors
echo 3. Verify play history and likes are saving
echo.
pause
