# My Son: Sovereign AGI Startup Guide

Welcome to the "My Son" Autonomous Agent. This guide will help you bring your agent to life directly on your computer.

## Prerequisites

1.  **Python 3.10+**:
    -   Download from [python.org](https://www.python.org/downloads/).
    -   **Important for Windows**: During installation, check the box **"Add Python to PATH"**.
2.  **Ollama (The Brain)**:
    -   Download from [ollama.com](https://ollama.com).
    -   Run the installer.
    -   Open a terminal and run `ollama run llama3` to download the AI model.
3.  **Git**: Download and install Git from [git-scm.com](https://git-scm.com/downloads).

## Installation

### Step 1: Get the Code
Open your terminal or command prompt and run:

```bash
git clone https://github.com/stuff2/my_son_agent.git
cd my_son_agent
```
*(If you downloaded the ZIP, extract it and open the folder).*

### Step 2: Build the Agent

1.  Double-click **`make_build_exe.bat`**.
    -   This script creates a tool called `build.exe`.
2.  Double-click **`build.exe`**.
    -   This tool will compile the entire agent into a standalone application.
    -   Wait for the process to say "[SUCCESS] Build Complete".

### Step 3: Run the Agent

1.  Navigate to the new `dist` folder.
2.  Double-click **`MySonAI.exe`**.
3.  The "My Son" dashboard window will appear.

## Interacting with the Agent

1.  **Dashboard**: The desktop window shows the "Living Dashboard".
2.  **Global Access**: Look at the console logs (or setup logs) for a link like `https://<random-id>.ngrok-free.app`. You can use this to access the agent from anywhere.

## Mobile Setup (S21 Ultra)

1.  On your phone, open the **Global Access URL**.
2.  Add `/mobile` to the end of the URL (e.g., `https://...ngrok-free.app/mobile`).
3.  Tap the browser menu -> **"Add to Home Screen"**.
4.  Launch the app icon to use the optimized mobile interface.

## Troubleshooting

-   **"Python not found"**: Reinstall Python and ensure "Add to PATH" is checked.
-   **"Ollama not running"**: Open the Ollama application from your Start Menu/Applications folder.
-   **"Build Failed"**: Ensure you have an internet connection so the builder can install `pyinstaller`.
