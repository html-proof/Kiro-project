@echo off
echo ========================================
echo Removing Dependent Projects
echo ========================================
echo.
echo This will remove:
echo - react-native-app/
echo - flutter-app/
echo - test-website/
echo - test-web-production/
echo.
echo Backend code will be preserved.
echo.
pause

echo Removing React Native app...
if exist "react-native-app" (
    rmdir /s /q react-native-app
    echo [OK] Removed react-native-app/
) else (
    echo [SKIP] react-native-app/ not found
)

echo Removing Flutter app...
if exist "flutter-app" (
    rmdir /s /q flutter-app
    echo [OK] Removed flutter-app/
) else (
    echo [SKIP] flutter-app/ not found
)

echo Removing test websites...
if exist "test-website" (
    rmdir /s /q test-website
    echo [OK] Removed test-website/
) else (
    echo [SKIP] test-website/ not found
)

if exist "test-web-production" (
    rmdir /s /q test-web-production
    echo [OK] Removed test-web-production/
) else (
    echo [SKIP] test-web-production/ not found
)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Removed directories have been deleted.
echo Backend code is intact.
echo.
echo To commit these changes:
echo   git add .
echo   git commit -m "chore: remove dependent projects, keep backend only"
echo   git push origin main
echo.
pause
