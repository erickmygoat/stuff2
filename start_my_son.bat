@echo off
setlocal

:: 1. Set Working Directory to Script Location
cd /d "%~dp0"

:: 2. Ensure PYTHONPATH includes current directory for subprocesses
set PYTHONPATH=%~dp0;%PYTHONPATH%

:: 3. Ensure UTF-8 output
set PYTHONUTF8=1

echo Initializing My Son (Windows Global Mode)...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python could not be found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b
)

:: Install Deps Globally (Directly to Computer)
echo Installing dependencies to your system Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please check your internet connection or Python installation.
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

:: Run
echo Starting Agent...
python main.py
pause
