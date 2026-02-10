@echo off
echo ========================================
echo   Building Musicly Flutter App
echo ========================================
echo.

set PROJECT_PATH=C:\Users\seban\personalprojects\musicly_app

REM Check if Flutter project exists
if not exist "%PROJECT_PATH%" (
    echo ERROR: Flutter project not found at %PROJECT_PATH%
    echo Please run: flutter create musicly_app
    pause
    exit /b 1
)

echo Flutter project found!
echo.

REM Create necessary directories
echo Creating directory structure...
mkdir "%PROJECT_PATH%\lib\core\config" 2>nul
mkdir "%PROJECT_PATH%\lib\core\di" 2>nul
mkdir "%PROJECT_PATH%\lib\core\network" 2>nul
mkdir "%PROJECT_PATH%\lib\features\splash" 2>nul
mkdir "%PROJECT_PATH%\lib\features\auth\presentation" 2>nul
mkdir "%PROJECT_PATH%\lib\features\home\presentation" 2>nul
mkdir "%PROJECT_PATH%\lib\features\search\presentation" 2>nul
mkdir "%PROJECT_PATH%\lib\shared\models" 2>nul
mkdir "%PROJECT_PATH%\lib\shared\services" 2>nul
mkdir "%PROJECT_PATH%\lib\shared\widgets" 2>nul
mkdir "%PROJECT_PATH%\assets\images" 2>nul

echo.
echo ========================================
echo   Copying Files...
echo ========================================
echo.

REM Copy pubspec.yaml
echo Copying pubspec.yaml...
copy /Y "flutter-app\pubspec.yaml" "%PROJECT_PATH%\pubspec.yaml"

REM Copy main.dart
echo Copying main.dart...
copy /Y "flutter-app\lib\main.dart" "%PROJECT_PATH%\lib\main.dart"

echo.
echo ========================================
echo   Files Copied Successfully!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Copy remaining code files from:
echo    flutter-app\COMPLETE_CODE_PACKAGE.md
echo.
echo 2. Add Firebase config:
echo    - Download google-services.json from Firebase Console
echo    - Place in: %PROJECT_PATH%\android\app\
echo.
echo 3. Install dependencies:
echo    cd %PROJECT_PATH%
echo    flutter pub get
echo.
echo 4. Run the app:
echo    flutter run
echo.
pause
