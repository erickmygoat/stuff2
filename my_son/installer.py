"""
This script installs the agent to a user directory and sets up the environment.
"""
import os
import shutil
import sys
import platform

APP_NAME = "MySon"
INSTALL_DIR = os.path.expanduser(f"~/.{APP_NAME.lower()}")

def install():
    print(f"Installing {APP_NAME} to {INSTALL_DIR}...")

    # 1. Create Directory
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)

    # 2. Copy Source Code
    current_dir = os.getcwd()
    print(f"Copying files from {current_dir}...")

    # Simple recursive copy
    # In a real scenario, we might want to exclude .git, venv, etc.
    # For this script, we assume it's running from the repo root.
    for item in os.listdir(current_dir):
        s = os.path.join(current_dir, item)
        d = os.path.join(INSTALL_DIR, item)
        if os.path.isdir(s):
            if item in [".git", "__pycache__", "venv", "verification"]:
                continue
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    print("Files copied.")

    # 3. Create Runner Script
    if platform.system() == "Windows":
        runner_path = os.path.join(INSTALL_DIR, "run_agent.bat")
        with open(runner_path, "w") as f:
            f.write("@echo off\n")
            f.write(f"cd {INSTALL_DIR}\n")
            f.write("python main.py\n")
            f.write("pause\n")
    else:
        runner_path = os.path.join(INSTALL_DIR, "run_agent.sh")
        with open(runner_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"cd {INSTALL_DIR}\n")
            f.write("python3 main.py\n")
        os.chmod(runner_path, 0o755)

    print(f"Installation complete. Run the agent using: {runner_path}")
    print("To enable auto-start, add this script to your startup items/cron.")

if __name__ == "__main__":
    install()
