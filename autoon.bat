@echo off
echo Adding Stock Analyzer Pro to Windows startup...
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Stock_Analyzer_Pro.lnk")
$Shortcut.TargetPath = "%USERPROFILE%\stock_analyzer\start.bat"
$Shortcut.WorkingDirectory = "%USERPROFILE%\stock_analyzer"
$Shortcut.Description = "Stock Analyzer Pro"
$Shortcut.Save()
echo Done! Stock Analyzer Pro will start with Windows.
pause
