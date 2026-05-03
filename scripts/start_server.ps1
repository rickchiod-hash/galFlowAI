$env:PATH = "K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio;" + $env:PATH
Set-Location K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta
Start-Process -FilePath "K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\python.exe" -ArgumentList "app\main.py" -NoNewWindow -PassThru
Start-Sleep 3
Invoke-WebRequest -Uri "http://127.0.0.1:7860" -UseBasicParsing