@echo off
echo Building My Son Desktop Executable...

:: Install PyInstaller if missing
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 pip install pyinstaller

:: Build
:: --noconsole: Hide terminal (remove if you want debugging)
:: --add-data: Include templates and static files
pyinstaller --noconfirm --onedir --console --name "MySonAI" ^
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

echo Build Complete. Check dist/MySonAI/MySonAI.exe
pause
