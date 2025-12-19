# My Son AGI - Deployment & Setup Guide

This guide explains how to set up, run, and compile the "My Son" Autonomous Agent as a standalone software application.

## 1. Prerequisites

Before running the agent, ensure you have:

1.  **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/). Ensure you check "Add Python to PATH" during installation.
2.  **Ollama (The Brain)**: The agent runs locally using Ollama.
    *   Download from [ollama.com](https://ollama.com).
    *   Run `ollama run llama3` (or your preferred model) in a separate terminal window to ensure the model is downloaded and the API is active.
3.  **Git** (Optional): To clone the repository, or just download the ZIP.

## 2. Quick Start (Desktop App)

The easiest way to run the agent is using the included batch script:

1.  Double-click **`start_desktop.bat`**.
2.  It will automatically:
    *   Install necessary dependencies (including `pywebview` for the GUI).
    *   Launch the **Launcher/Setup** window.
3.  In the Launcher:
    *   Check that "Agent Core" and "Brain" are green (Online).
    *   (Optional) Enter your **Ngrok Authtoken** if you want to control the agent remotely from your phone.
    *   Click **LAUNCH INTERFACE**.

## 3. Creating a Standalone EXE

You can compile the agent into a single folder/executable to share or run without opening terminals.

1.  Double-click **`build_exe.bat`**.
2.  Wait for the process to complete (it may take a few minutes).
3.  Once finished, navigate to the `dist/MySonAI` folder.
4.  Run **`MySonAI.exe`**.

## 4. Global Access (Mobile Control)

To control your agent from anywhere:

1.  Get a free Authtoken from [ngrok.com](https://ngrok.com).
2.  Enter it in the **Launcher** screen when you start the app.
3.  Once the interface loads, check the **Logs** (Right Panel) or the Console for the **Global Access URL** (e.g., `https://xxxx.ngrok-free.app`).
4.  Open that URL on your phone to access the Mobile Interface.

## 5. Troubleshooting

*   **"Brain Offline"**: Ensure Ollama is running (`ollama serve` or the desktop app).
*   **"Port already in use"**: Ensure no other instance of the agent is running on port 8000.
*   **White Screen / Connection Failed**: Ensure `start_desktop.bat` didn't close immediately due to an error. Run it from a terminal (cmd.exe) to see error messages.
