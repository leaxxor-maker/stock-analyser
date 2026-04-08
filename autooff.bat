@echo off
echo Removing Stock Analyzer Pro from Windows startup...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Stock_Analyzer_Pro.lnk" 2>nul
if %errorlevel%==0 (echo Removed successfully!) else (echo Not found in startup.)
pause
