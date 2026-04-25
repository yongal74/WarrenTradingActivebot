@echo off
cd /d "%~dp0"
echo ============================================================
echo   ngrok - TradingView External Tunnel
echo ============================================================
echo.

where ngrok > nul 2>&1
if errorlevel 1 (
    echo [ERROR] ngrok not found.
    echo.
    echo   1. Download from https://ngrok.com/download
    echo   2. Copy ngrok.exe to this folder or add to PATH
    echo   3. Run this file again
    echo.
    pause & exit /b 1
)

echo Starting ngrok on port 8080...
echo.
echo   Copy the "Forwarding" URL and paste it into TradingView Alert URL:
echo   Example: https://xxxx-xx-xxx.ngrok-free.app/webhook
echo.
ngrok http 8080
pause
