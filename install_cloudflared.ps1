# One-time setup for cloud access
$ProgressPreference = 'SilentlyContinue'
Write-Host "Downloading cloudflared..."
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "C:\stock_analyzer\cloudflared.exe"
Write-Host "Done! Now run: cloud_run.bat"
pause
