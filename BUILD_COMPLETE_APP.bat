@echo off
echo ========================================
echo   Building Complete Musicly Flutter App
echo ========================================
echo.

set SRC=flutter-app
set DEST=..\musicly_app

REM Check if destination exists
if not exist "%DEST%" (
    echo ERROR: Flutter project not found!
    echo.
    echo Creating Flutter project...
    cd ..
    flutter create musicly_app
    cd musicly-backend
    set DEST=..\musicly_app
)

echo.
echo Copying ALL files to: %DEST%
echo.

REM Create ALL directories
echo Creating directory structure...
mkdir "%DEST%\lib\core\config" 2>nul
mkdir "%DEST%\lib\core\di" 2>nul
mkdir "%DEST%\lib\features\splash" 2>nul
mkdir "%DEST%\lib\features\auth\presentation" 2>nul
mkdir "%DEST%\lib\features\home\presentation" 2>nul
mkdir "%DEST%\lib\features\search\presentation" 2>nul
mkdir "%DEST%\assets\images" 2>nul

echo.
echo Copying files...
echo.

REM Copy pubspec.yaml
echo [1/10] pubspec.yaml
copy /Y "%SRC%\pubspec.yaml" "%DEST%\pubspec.yaml" >nul

REM Copy main.dart
echo [2/10] main.dart
copy /Y "%SRC%\lib\main.dart" "%DEST%\lib\main.dart" >nul

REM Copy config files
echo [3/10] api_config.dart
copy /Y "%SRC%\lib\core\config\api_config.dart" "%DEST%\lib\core\config\api_config.dart" >nul

echo [4/10] theme_config.dart
copy /Y "%SRC%\lib\core\config\theme_config.dart" "%DEST%\lib\core\config\theme_config.dart" >nul

echo [5/10] injection.dart
copy /Y "%SRC%\lib\core\di\injection.dart" "%DEST%\lib\core\di\injection.dart" >nul

REM Copy feature files
echo [6/10] splash_screen.dart
copy /Y "%SRC%\lib\features\splash\splash_screen.dart" "%DEST%\lib\features\splash\splash_screen.dart" >nul

echo [7/10] login_screen.dart
copy /Y "%SRC%\lib\features\auth\presentation\login_screen.dart" "%DEST%\lib\features\auth\presentation\login_screen.dart" >nul

echo [8/10] home_screen.dart
copy /Y "%SRC%\lib\features\home\presentation\home_screen.dart" "%DEST%\lib\features\home\presentation\home_screen.dart" >nul

echo [9/10] search_screen.dart
copy /Y "%SRC%\lib\features\search\presentation\search_screen.dart" "%DEST%\lib\features\search\presentation\search_screen.dart" >nul

echo [10/10] Done!

echo.
echo ========================================
echo   ✅ ALL FILES COPIED SUCCESSFULLY!
echo ========================================
echo.
echo Your Flutter app is ready at:
echo   %DEST%
echo.
echo Next Steps:
echo.
echo 1. Add Firebase Configuration:
echo    - Download google-services.json from Firebase Console
echo    - Place in: %DEST%\android\app\
echo.
echo 2. Install Dependencies:
echo    cd %DEST%
echo    flutter pub get
echo.
echo 3. Run the App:
echo    flutter run
echo.
echo 4. Build APK:
echo    flutter build apk --release
echo.
echo ========================================
echo   Your Backend is Live:
echo   https://web-production-1dedc.up.railway.app
echo ========================================
echo.
pause
