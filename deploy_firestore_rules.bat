@echo off
REM Firestore Rules Deployment Script for Windows
REM This script helps you deploy Firestore security rules

echo.
echo 🔒 Firestore Rules Deployment
echo ==============================
echo.

REM Check if Firebase CLI is installed
where firebase >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Firebase CLI not found!
    echo.
    echo Install it with:
    echo   npm install -g firebase-tools
    echo.
    pause
    exit /b 1
)

echo ✅ Firebase CLI found
echo.

REM Check if logged in
echo Checking Firebase login status...
firebase projects:list >nul 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Not logged in to Firebase
    echo.
    echo Please login:
    firebase login
    echo.
)

echo ✅ Logged in to Firebase
echo.

REM Show current project
echo Current Firebase project:
firebase use
echo.

REM Ask for confirmation
echo 📋 This will deploy the rules from: firestore.rules
echo.
set /p CONFIRM="Continue? (y/n): "

if /i not "%CONFIRM%"=="y" (
    echo ❌ Deployment cancelled
    pause
    exit /b 1
)

REM Deploy rules
echo.
echo 🚀 Deploying Firestore rules...
firebase deploy --only firestore:rules

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Rules deployed successfully!
    echo.
    echo 🔗 View rules at:
    echo    https://console.firebase.google.com/project/music-app-f2e65/firestore/rules
    echo.
    echo 🧪 Test rules at:
    echo    https://console.firebase.google.com/project/music-app-f2e65/firestore/rules
    echo    (Click 'Rules Playground' tab^)
    echo.
) else (
    echo.
    echo ❌ Deployment failed!
    echo.
    echo Try deploying manually:
    echo 1. Go to: https://console.firebase.google.com/project/music-app-f2e65/firestore/rules
    echo 2. Copy contents from firestore.rules
    echo 3. Paste and click 'Publish'
    echo.
)

pause
