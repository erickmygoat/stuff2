@echo off
echo ==========================================
echo    Compiling Builder Utility...
echo ==========================================

:: Ensure PyInstaller is ready
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 pip install pyinstaller

:: Compile builder.py into build.exe
pyinstaller --noconfirm --onefile --console --name "build" builder.py

:: Cleanup artifacts
if exist dist\build.exe (
    move /Y dist\build.exe .
    rd /s /q build dist
    del /f /q build.spec
    echo.
    echo [SUCCESS] build.exe created successfully.
    echo You can now delete this bat file and builder.py if desired.
) else (
    echo.
    echo [ERROR] Failed to create build.exe.
)

pause
