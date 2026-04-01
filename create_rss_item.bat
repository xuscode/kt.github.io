@echo off
echo Creating RSS item...

REM Run creation script
D:\python_env\python-3.12.4-embed-amd64\python.exe create_rss_item.py

if errorlevel 1 (
    echo Creation failed!
    pause
    exit /b 1
)

echo Creation successful!
pause