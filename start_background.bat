@echo off
REM Start Zama Bot in Background (Windows)
REM This keeps the bot running even after closing the window

echo Starting Zama Telegram Bot in background...

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Start bot with pythonw (no window)
start /B venv\Scripts\pythonw.exe bot.py

echo.
echo Bot started in background!
echo.
echo To stop the bot:
echo 1. Open Task Manager (Ctrl+Shift+Esc)
echo 2. Find "pythonw.exe" process
echo 3. End task
echo.
echo To view logs:
echo Open: bot.log
echo.

timeout /t 5


