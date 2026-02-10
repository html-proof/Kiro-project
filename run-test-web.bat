@echo off
echo Starting Musicly Test Web Interface...
echo.
echo Make sure your backend is running on http://localhost:8000
echo.
echo Opening test interface in your default browser...
echo.

start test-web\index.html

echo.
echo Test interface opened!
echo.
echo If the backend is not running, start it with:
echo   python -m uvicorn app.main:app --reload --port 8000
echo.
pause
