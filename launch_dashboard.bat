@echo off
cd /d %~dp0
echo [⚙️] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo [🚀] Launching Streamlit dashboard...
streamlit run dashboard.py

pause
