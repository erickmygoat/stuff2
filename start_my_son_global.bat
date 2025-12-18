@echo off
setlocal
set PYTHONUTF8=1

echo Initializing My Son (Global Mode)...

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found.
    pause
    exit /b
)

:: Install Dependencies Globally
echo Installing dependencies to system Python...
pip install -r requirements.txt

:: Check Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama not running. Brain will be offline.
    timeout /t 3
)

:: Run
echo Starting Agent...
python main.py
pause
