@echo off
cd /d "%~dp0"

echo ============================================================
echo   WarrenTradingActivebot - Release
echo ============================================================
echo.

if "%1"=="" (
    echo Usage: release.bat [version] [message]
    echo Example: release.bat 1.1.0 "Add TradingView Pine Script"
    echo.
    pause & exit /b 1
)

set VERSION=%1
set MSG=%~2
if "%MSG%"=="" set MSG=Release v%VERSION%

echo [1/4] Updating version.py...
powershell -Command "(Get-Content version.py) -replace '__version__ = \".*\"', '__version__ = \"%VERSION%\"' -replace '__release_date__ = \".*\"', '__release_date__ = \"' + (Get-Date -Format 'yyyy-MM-dd') + '\"' | Set-Content version.py"

echo [2/4] Git commit and tag...
git add -A
git commit -m "Release v%VERSION%: %MSG%"
git tag -a v%VERSION% -m "v%VERSION% - %MSG%"

echo [3/4] Push to GitHub...
git push origin master
git push origin v%VERSION%

echo [4/4] Create GitHub Release...
gh release create v%VERSION% --title "WarrenTradingActivebot v%VERSION%" --generate-notes

echo.
echo Release complete!
echo https://github.com/yongal74/WarrenTradingActivebot/releases/tag/v%VERSION%
echo.
pause
