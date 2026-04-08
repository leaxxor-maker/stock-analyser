@echo off
cd /d "%~dp0"

echo ================================================
echo    STARTING STOCK ANALYZER
echo ================================================
echo.

start "Stock Server" cmd /k "python stock_analyzer.py"

timeout /t 3 /nobreak >nul

echo Waiting for tunnel URL...
echo.

start "Cloudflare" cmd /k "cloudflared.exe tunnel --url http://localhost:5000"

echo.
echo ================================================
echo  Wait 10 seconds, COPY the URL from the
echo  Cloudflare window, then paste in browser
echo ================================================
echo.
echo Example: https://abc-123-xyz.trycloudflare.com
echo.
pause
