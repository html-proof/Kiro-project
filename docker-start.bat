@echo off
REM Quick Docker Start Script for Windows

echo.
echo 🐳 Musicly Backend - Docker Quick Start
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your Firebase credentials!
    echo.
    pause
    exit /b 1
)

echo ✅ .env file found
echo.

REM Ask which mode
echo Choose mode:
echo   1. Production (optimized)
echo   2. Development (hot reload + Redis Commander)
echo.
set /p MODE="Enter choice (1 or 2): "

if "%MODE%"=="2" (
    echo.
    echo 🚀 Starting in DEVELOPMENT mode...
    echo.
    docker-compose -f docker-compose.dev.yml up -d
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ Services started successfully!
        echo.
        echo 📍 Access points:
        echo    - Backend API: http://localhost:8000
        echo    - API Docs: http://localhost:8000/docs
        echo    - Redis Commander: http://localhost:8081
        echo.
        echo 📋 Useful commands:
        echo    - View logs: docker-compose -f docker-compose.dev.yml logs -f
        echo    - Stop: docker-compose -f docker-compose.dev.yml down
        echo.
    )
) else (
    echo.
    echo 🚀 Starting in PRODUCTION mode...
    echo.
    docker-compose up -d
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ Services started successfully!
        echo.
        echo 📍 Access points:
        echo    - Backend API: http://localhost:8000
        echo    - API Docs: http://localhost:8000/docs
        echo.
        echo 📋 Useful commands:
        echo    - View logs: docker-compose logs -f
        echo    - Stop: docker-compose down
        echo.
    )
)

echo 🧪 Testing backend...
timeout /t 5 /nobreak >nul
curl -s http://localhost:8000/health

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Backend is healthy!
) else (
    echo.
    echo ⚠️  Backend not responding yet. Check logs:
    echo    docker-compose logs -f backend
)

echo.
pause
