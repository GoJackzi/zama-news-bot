#!/bin/bash

echo "========================================"
echo "Zama Telegram News Bot"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo
    echo "Please create a .env file with your configuration."
    echo "See SETUP_GUIDE.md for instructions."
    echo
    exit 1
fi

# Install/update requirements
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo
echo "Starting bot..."
echo "Press Ctrl+C to stop"
echo

python3 bot.py

