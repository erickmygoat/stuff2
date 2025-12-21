@echo off
echo ==================================================
echo    Creating Launcher.exe (My Son AGI)
echo ==================================================

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ and check "Add to PATH".
    pause
    exit /b
)

:: 2. Install Dependencies
echo.
echo [1/3] Installing system dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

:: 3. Build Launcher.exe
echo.
echo [2/3] Compiling Launcher.exe...

:: Ensure static directory exists (PyInstaller fails if missing)
if not exist static mkdir static

:: Using 'python -m PyInstaller' avoids "command not found" errors
python -m PyInstaller --noconfirm --onefile --noconsole --name "Launcher" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import "uvicorn.logging" ^
    --hidden-import "uvicorn.loops" ^
    --hidden-import "uvicorn.loops.auto" ^
    --hidden-import "uvicorn.protocols" ^
    --hidden-import "uvicorn.protocols.http" ^
    --hidden-import "uvicorn.protocols.http.auto" ^
    --hidden-import "uvicorn.lifespan" ^
    --hidden-import "uvicorn.lifespan.on" ^
    --hidden-import "engineio.async_drivers.aiohttp" ^
    desktop.py

:: 4. Cleanup and Move
echo.
echo [3/3] Finalizing...
if exist dist\Launcher.exe (
    move /Y dist\Launcher.exe .
    rmdir /s /q build dist
    del /f /q Launcher.spec
    echo.
    echo ==================================================
    echo    SUCCESS! Launcher.exe created.
    echo ==================================================
    echo You can now double-click 'Launcher.exe' to start the agent.
) else (
    echo.
    echo [ERROR] Build failed. Please check the logs above.
)

pause
