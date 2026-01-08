# Start backend uvicorn and frontend static server in separate powershell windows
$backendCmd = "$env:PYTHONPATH='$(Resolve-Path backend).Path'; python -m uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

$frontendCmd = "python -m http.server 5500 --directory frontend/public"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host "Started backend and frontend in new windows. Open http://localhost:5500/ to use the UI."
