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

### Step 2: Start the Agent

#### On Windows (One-Click Global Mode)
1.  Double-click `start_my_son.bat`.
2.  This script will:
    -   Check if Python and Ollama are ready.
    -   Install all necessary libraries directly to your computer.
    -   Launch the agent.

#### On Mac/Linux
1.  Open a terminal in the folder.
2.  Run:
    ```bash
    chmod +x start_my_son_global.sh
    ./start_my_son_global.sh
    ```

## Interacting with the Agent

Once the console says **"Starting My Son Agent Server..."**:

1.  **Dashboard**: Open `http://localhost:8000` in your web browser. You will see the "Living Dashboard".
2.  **Global Access**: Look at the console output for a link like `https://<random-id>.ngrok-free.app`. You can use this to access the agent from anywhere.

## Mobile Setup (S21 Ultra)

1.  On your phone, open the **Global Access URL** (from the console logs).
2.  Add `/mobile` to the end of the URL (e.g., `https://...ngrok-free.app/mobile`).
3.  Tap the browser menu -> **"Add to Home Screen"**.
4.  Launch the app icon to use the optimized mobile interface.

## Troubleshooting

-   **"Python not found"**: Reinstall Python and ensure "Add to PATH" is checked.
-   **"Ollama not running"**: Open the Ollama application from your Start Menu/Applications folder.
-   **Audio issues**: Ensure your speakers are on. On Windows, the agent uses the native system voice.
