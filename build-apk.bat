@echo off
echo ========================================
echo   Building Musicly APK
echo ========================================
echo.

cd ..\musicly_app

echo Cleaning previous builds...
flutter clean

echo.
echo Installing dependencies...
flutter pub get

echo.
echo ========================================
echo   Building Release APK...
echo ========================================
echo.

REM Build release APK with split per ABI for smaller size
flutter build apk --release --split-per-abi

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Your APKs are located at:
echo   build\app\outputs\flutter-apk\
echo.
echo Files created:
dir build\app\outputs\flutter-apk\*.apk /b
echo.
echo Install on device:
echo   adb install build\app\outputs\flutter-apk\app-armeabi-v7a-release.apk
echo.
pause
