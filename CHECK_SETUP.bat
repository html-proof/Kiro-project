@echo off
echo ========================================
echo Musicly Backend - Setup Checker
echo ========================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found
    echo Please install Python 3.8+ from https://www.python.org/
) else (
    python --version
    echo [OK] Python installed
)
echo.

REM Check pip
echo [2/6] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] pip not found
) else (
    pip --version
    echo [OK] pip installed
)
echo.

REM Check virtual environment
echo [3/6] Checking virtual environment...
if exist "venv" (
    echo [OK] Virtual environment exists
) else (
    echo [WARN] Virtual environment not found
    echo Run BUILD_AND_RUN.bat to create it
)
echo.

REM Check .env file
echo [4/6] Checking .env file...
if exist ".env" (
    echo [OK] .env file exists
) else (
    echo [WARN] .env file not found
    echo Copy .env.example to .env and configure it
)
echo.

REM Check Firebase credentials
echo [5/6] Checking Firebase credentials...
if exist "app\music-app-f2e65-firebase-adminsdk-fbsvc-8787f0f5e5.json" (
    echo [OK] Firebase credentials file exists
) else (
    echo [WARN] Firebase credentials not found
    echo Download from Firebase Console and place in app/ folder
)
echo.

REM Check requirements
echo [6/6] Checking installed packages...
if exist "venv" (
    call venv\Scripts\activate.bat
    pip list | findstr "fastapi uvicorn firebase-admin" >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Some packages may be missing
        echo Run BUILD_AND_RUN.bat to install dependencies
    ) else (
        echo [OK] Core packages installed
    )
) else (
    echo [SKIP] Virtual environment not found
)
echo.

echo ========================================
echo Setup check complete!
echo ========================================
echo.
echo Next steps:
echo 1. If any checks failed, fix them first
echo 2. Run BUILD_AND_RUN.bat to build and start server
echo 3. Or run QUICK_RUN.bat if already built
echo.
pause
