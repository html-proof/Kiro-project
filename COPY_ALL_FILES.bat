@echo off
echo ========================================
echo   Copying ALL Flutter Files
echo ========================================
echo.

set SRC=flutter-app
set DEST=..\musicly_app

REM Check if destination exists
if not exist "%DEST%" (
    echo ERROR: Flutter project not found!
    echo Please ensure musicly_app exists at: %DEST%
    pause
    exit /b 1
)

echo Copying files to: %DEST%
echo.

REM Copy pubspec.yaml
echo [1/12] Copying pubspec.yaml...
copy /Y "%SRC%\pubspec.yaml" "%DEST%\pubspec.yaml" >nul

REM Copy main.dart
echo [2/12] Copying main.dart...
copy /Y "%SRC%\lib\main.dart" "%DEST%\lib\main.dart" >nul

REM Create directories
echo [3/12] Creating directories...
mkdir "%DEST%\lib\core\config" 2>nul
mkdir "%DEST%\lib\core\di" 2>nul
mkdir "%DEST%\lib\features\splash" 2>nul
mkdir "%DEST%\lib\features\auth\presentation" 2>nul
mkdir "%DEST%\lib\features\home\presentation" 2>nul
mkdir "%DEST%\lib\features\search\presentation" 2>nul

REM Copy config files
echo [4/12] Copying api_config.dart...
copy /Y "%SRC%\lib\core\config\api_config.dart" "%DEST%\lib\core\config\api_config.dart" >nul

echo [5/12] Copying theme_config.dart...
copy /Y "%SRC%\lib\core\config\theme_config.dart" "%DEST%\lib\core\config\theme_config.dart" >nul

echo [6/12] Copying injection.dart...
copy /Y "%SRC%\lib\core\di\injection.dart" "%DEST%\lib\core\di\injection.dart" >nul

echo.
echo ========================================
echo   ✅ Core Files Copied!
echo ========================================
echo.
echo Remaining files are in:
echo   flutter-app\COMPLETE_CODE_PACKAGE.md
echo.
echo Copy these manually:
echo   - lib\features\splash\splash_screen.dart
echo   - lib\features\auth\presentation\login_screen.dart
echo   - lib\features\home\presentation\home_screen.dart
echo   - lib\features\search\presentation\search_screen.dart
echo.
echo Then run:
echo   cd %DEST%
echo   flutter pub get
echo   flutter run
echo.
pause
