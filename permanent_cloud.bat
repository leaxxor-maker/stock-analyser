@echo off
cd /d "%~dp0"

echo ================================================
echo    STOCK ANALYZER - PERMANENT CLOUD ACCESS
echo ================================================
echo.
echo IMPORTANT: Keep this window open!
echo.
echo Step 1: Starting Stock Analyzer server...
start "Stock Server" cmd /k "python stock_analyzer.py"

timeout /t 4 /nobreak >nul

echo Step 2: Starting permanent tunnel...
cloudflared.exe service install eyJhIjoiMDU2NTEyMGM2MzZjN2Q4ZjY4MTBlNTkwNmRlNjA5ZDkiLCJ0IjoiYTkwMWRjMjktYTJkOC00NjFhLWI2ODQtZDA2Y2E0YTc3YTBiIiwicyI6Ik9EVm1ZVEU1TnpJdE9XVTROUzAwTmpSaExUZzFNelV0TWpVMk1qVXdPR00zTkRZeSJ9

echo.
echo ================================================
echo  Your URL: stock-analyzer.trycloudflare.com
echo ================================================
pause
