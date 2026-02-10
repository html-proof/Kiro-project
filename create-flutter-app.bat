@echo off
echo ========================================
echo   Musicly Flutter App - Quick Setup
echo ========================================
echo.

REM Check if Flutter is installed
flutter --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Flutter is not installed!
    echo Please install Flutter from: https://flutter.dev/docs/get-started/install
    pause
    exit /b 1
)

echo Flutter is installed!
echo.

REM Navigate to parent directory
cd ..

REM Create Flutter project
echo Creating Flutter project...
flutter create musicly_app

REM Navigate into project
cd musicly_app

echo.
echo ========================================
echo   Project Created Successfully!
echo ========================================
echo.
echo Next Steps:
echo 1. Copy code files from FLUTTER_COMPLETE_CODE.md
echo 2. Update pubspec.yaml with dependencies
echo 3. Add Firebase config files
echo 4. Run: flutter pub get
echo 5. Run: flutter run
echo.
echo Full guide: ../musicly-backend/FLUTTER_APP_SETUP.md
echo.
pause
