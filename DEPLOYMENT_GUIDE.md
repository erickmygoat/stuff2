# My Son AGI - Deployment & Setup Guide

This guide explains how to set up, run, and compile the "My Son" Autonomous Agent as a standalone software application.

## 1. Prerequisites

Before running the agent, ensure you have:

1.  **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/). Ensure you check "Add Python to PATH" during installation.
2.  **Ollama (The Brain)**: The agent runs locally using Ollama.
    *   Download from [ollama.com](https://ollama.com).
    *   Run `ollama run llama3` (or your preferred model) in a separate terminal window.

## 2. Creating the Standalone EXE

You can compile the agent into a single executable to run without opening terminals.

1.  **One-Time Setup**: Double-click **`make_build_exe.bat`**.
    *   This creates the `build.exe` utility.
2.  **Build Agent**: Double-click **`build.exe`**.
    *   This compiles the source code into `dist/MySonAI.exe`.
3.  **Run**: Open `dist/MySonAI.exe`.

## 3. Global Access (Mobile Control)

To control your agent from anywhere:

1.  Get a free Authtoken from [ngrok.com](https://ngrok.com).
2.  Enter it in the **Launcher** screen when you start the app.
3.  Once the interface loads, check the **Logs** (Right Panel) for the **Global Access URL** (e.g., `https://xxxx.ngrok-free.app`).
4.  Open that URL on your phone to access the Mobile Interface.

## 4. Troubleshooting

*   **"Brain Offline"**: Ensure Ollama is running (`ollama serve` or the desktop app).
*   **"Port already in use"**: Ensure no other instance of the agent is running on port 8000.
*   **Build Error**: Ensure you have write permissions in the folder.
