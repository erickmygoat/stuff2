@echo off
setlocal

:: 1. Set Working Directory to Script Location
cd /d "%~dp0"

:: 2. Ensure PYTHONPATH includes current directory
set PYTHONPATH=%~dp0;%PYTHONPATH%

:: 3. Ensure UTF-8 output
set PYTHONUTF8=1

echo Starting My Son Desktop App...

:: Check for pywebview
pip show pywebview >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Desktop App dependencies...
    pip install pywebview
)

:: Run Desktop App
python desktop.py
pause
