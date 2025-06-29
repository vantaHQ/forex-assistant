@echo off
cd /d %~dp0

echo Creating folders...
mkdir data
mkdir signals
mkdir modules
mkdir core

echo Installing dependencies...
pip install -r requirements.txt

echo ✓ Setup complete. Launch with: python main.py
pause
