@echo off
cd /d "%~dp0"

echo ================================================
echo    STOCK ANALYZER - CLOUD ACCESS
echo ================================================
echo.

echo [1/2] Starting server...
start "Server" cmd /k "python stock_analyzer.py"

timeout /t 3 /nobreak >nul

echo [2/2] Creating tunnel...
start "Cloudflare" cmd /k "cloudflared.exe tunnel --url http://localhost:5000"

echo.
echo ================================================
echo    OPEN THE LINK SHOWN IN 'Cloudflare' WINDOW
echo ================================================
pause
