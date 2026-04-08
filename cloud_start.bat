@echo off
cd /d "%~dp0"

echo ================================================
echo    STOCK ANALYZER - CLOUD ACCESS
echo ================================================
echo.
echo Starting server and tunnel...
echo.

start "Stock Server" cmd /k "python stock_analyzer.py"

timeout /t 3 /nobreak >nul

start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel run --token eyJhIjoiMDU2NTEyMGM2MzZjN2Q4ZjY4MTBlNTkwNmRlNjA5ZDkiLCJ0IjoiYTkwMWRjMjktYTJkOC00NjFhLWI2ODQtZDA2Y2E0YTc3YTBiIiwicyI6Ik9EVm1ZVEU1TnpJdE9XVTROUzAwTmpSaExUZzFNelV0TWpVMk1qVXdPR00zTkRZeSJ9"

echo.
echo Wait 10 seconds, then open:
echo https://stock-analyzer.trycloudflare.com
echo.
pause
