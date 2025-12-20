import os
import subprocess
import sys
import shutil

def main():
    print("==========================================")
    print("   My Son: Sovereign AGI - Builder Protocol")
    print("==========================================")

    # 1. Check/Install PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print(">> Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Define Build Command
    print(">> Compiling Source Code...")
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--noconsole",
        "--name", "MySonAI",
        "--add-data", "templates;templates",
        "--add-data", "static;static",
        # Explicit hidden imports for Uvicorn & EngineIO
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "engineio.async_drivers.aiohttp",
        "desktop.py"
    ]

    # 3. Execute Build
    try:
        subprocess.check_call(cmd)
        print("\n[SUCCESS] Build Complete.")

        dist_path = os.path.abspath("dist/MySonAI.exe")
        if os.path.exists(dist_path):
            print(f"Target: {dist_path}")
            print("You may now move this file anywhere and run it.")
        else:
            print("[WARNING] Build finished but EXE not found. Check 'dist/' folder.")

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build Failed: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    print("\nPress Enter to close builder...")
    input()

if __name__ == "__main__":
    main()
