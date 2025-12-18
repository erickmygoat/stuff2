@echo off
setlocal
:: Ensure UTF-8 output for emojis
set PYTHONUTF8=1

echo Initializing My Son (Windows Mode)...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python could not be found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b
)

:: Check for Virtual Environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate Venv
call venv\Scripts\activate

:: Install Deps
echo Checking dependencies...
pip install -r requirements.txt

:: Check Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama does not seem to be running on port 11434.
    echo Please ensure Ollama is started in another window for the Brain to work.
    timeout /t 5
)

:: Run
echo Starting Agent...
python main.py
pause
