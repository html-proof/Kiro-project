@echo off
echo ========================================
echo Copying React Native App Files
echo ========================================
echo.

set SOURCE=musicly-backend\react-native-app
set DEST=C:\Users\seban\personalprojects\musicly-rn

echo Copying files from %SOURCE% to %DEST%...
echo.

REM Copy main files
copy "%SOURCE%\App.js" "%DEST%\App.js" /Y
copy "%SOURCE%\package.json" "%DEST%\package.json" /Y
copy "%SOURCE%\app.json" "%DEST%\app.json" /Y
copy "%SOURCE%\.gitignore" "%DEST%\.gitignore" /Y

REM Create directories
if not exist "%DEST%\src\config" mkdir "%DEST%\src\config"
if not exist "%DEST%\src\screens" mkdir "%DEST%\src\screens"

REM Copy config files
copy "%SOURCE%\src\config\firebase.js" "%DEST%\src\config\firebase.js" /Y
copy "%SOURCE%\src\config\api.js" "%DEST%\src\config\api.js" /Y

REM Copy screen files
copy "%SOURCE%\src\screens\SplashScreen.js" "%DEST%\src\screens\SplashScreen.js" /Y
copy "%SOURCE%\src\screens\LoginScreen.js" "%DEST%\src\screens\LoginScreen.js" /Y
copy "%SOURCE%\src\screens\WelcomeScreen.js" "%DEST%\src\screens\WelcomeScreen.js" /Y

echo.
echo ========================================
echo ✅ Files copied successfully!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Update src\config\firebase.js with your Firebase credentials
echo 2. Run: cd %DEST%
echo 3. Run: npm install
echo 4. Run: npm start
echo.
pause
