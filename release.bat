@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo   WarrenTradingActivebot - 버전 릴리즈
echo ============================================================
echo.

if "%1"=="" (
    echo 사용법: release.bat [버전] [설명]
    echo 예시:   release.bat 1.1.0 "TradingView Pine Script 추가"
    echo.
    pause & exit /b 1
)

set VERSION=%1
set MSG=%~2
if "%MSG%"=="" set MSG=Release v%VERSION%

echo [1/4] version.py 업데이트 중...
powershell -Command "(Get-Content version.py) -replace '__version__ = \".*\"', '__version__ = \"%VERSION%\"' -replace '__release_date__ = \".*\"', '__release_date__ = \"' + (Get-Date -Format 'yyyy-MM-dd') + '\"' | Set-Content version.py"

echo [2/4] git 커밋 및 태그...
git add -A
git commit -m "Release v%VERSION%: %MSG%"
git tag -a v%VERSION% -m "v%VERSION% - %MSG%"

echo [3/4] GitHub 푸시...
git push origin master
git push origin v%VERSION%

echo [4/4] GitHub 릴리즈 생성...
gh release create v%VERSION% --title "WarrenTradingActivebot v%VERSION%" --generate-notes

echo.
echo 릴리즈 완료!
echo https://github.com/yongal74/WarrenTradingActivebot/releases/tag/v%VERSION%
echo.
pause
