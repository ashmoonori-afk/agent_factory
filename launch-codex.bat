@echo off
REM Agent Factory — Launch with Codex (Windows)
REM Double-click this file to open Agent Factory in Codex.

cd /d "%~dp0"

echo =========================================
echo   Agent Factory — Starting Codex
echo =========================================
echo.
echo   Project: %CD%
echo   Codex will read CODEX.md automatically.
echo.

where codex >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'codex' command not found.
    echo   Install Codex: https://github.com/openai/codex
    echo.
    pause
    exit /b 1
)

codex

echo.
echo Session ended.
pause
