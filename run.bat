@echo off
echo ========================================
echo Zama Telegram News Bot
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file with your configuration.
    echo See SETUP_GUIDE.md for instructions.
    echo.
    pause
    exit /b 1
)

REM Install/update requirements
echo Checking dependencies...
pip install -q -r requirements.txt

echo.
echo Starting bot...
echo Press Ctrl+C to stop
echo.

python bot.py

pause

