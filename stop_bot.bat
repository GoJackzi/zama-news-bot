@echo off
REM Stop all pythonw.exe processes (stops background bot)

echo Stopping Zama Telegram Bot...
taskkill /F /IM pythonw.exe 2>nul

if %ERRORLEVEL% EQU 0 (
    echo Bot stopped successfully!
) else (
    echo No bot process found running.
)

echo.
pause


