@echo off
cd /d "%~dp0"

echo.
echo ============================================================
echo   WarrenTradingActivebot - Install
echo ============================================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo   Please install Python 3.11+ from https://python.org
    echo   Make sure to check "Add Python to PATH"
    pause & exit /b 1
)
echo [OK] Python found

echo.
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip -q

echo [2/4] Installing packages... (this may take a few minutes)
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] Package install failed. Check requirements.txt
    pause & exit /b 1
)
echo [OK] Packages installed

echo [3/4] Creating folders...
if not exist logs mkdir logs
if not exist reports mkdir reports
if not exist data\cache mkdir data\cache
if not exist backtest_results mkdir backtest_results
echo [OK] Folders created

echo [4/4] Setting up .env...
if not exist .env (
    copy .env.example .env > nul
    echo [OK] .env created - please edit it before running
) else (
    echo [OK] .env already exists
)

echo.
echo ============================================================
echo   Install complete!
echo ============================================================
echo.
echo   Next steps:
echo   1. Open .env and set PAPER_CAPITAL (default: 10000000)
echo   2. Double-click run_dashboard.bat
echo      -> Open browser: http://localhost:8501
echo   3. Double-click run_bot.bat to run once manually
echo.
pause
