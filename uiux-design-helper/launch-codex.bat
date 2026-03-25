@echo off
REM uiux-design-helper — Launch with Codex (Windows)
REM Double-click this file to start your agent.

cd /d "%~dp0"

echo =========================================
echo   uiux-design-helper — Starting Codex
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
