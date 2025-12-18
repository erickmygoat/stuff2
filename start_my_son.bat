@echo off
setlocal
:: Ensure UTF-8 output for emojis
set PYTHONUTF8=1

echo Initializing My Son...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python could not be found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b
)

:: Check for Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama does not seem to be running on port 11434.
    echo Please ensure Ollama is started in another window for the Brain to work.
    timeout /t 5
)

:: Check if user wants global or venv mode (Defaulting to Global for single-file simplicity)
:: But robust way is to try venv first, if fails or not desired, fallback.
:: The prompt asked for "only one file" for launching on Windows.
:: I will consolidate the logic: Check/Create Venv -> Install Deps -> Run.

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate Venv
call venv\Scripts\activate

:: Install Deps
echo Checking dependencies...
pip install -r requirements.txt

:: Run
echo Starting Agent...
python main.py
pause
