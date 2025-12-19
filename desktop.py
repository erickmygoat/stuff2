import sys
import threading
import time
import webview
import uvicorn
import os

# Ensure we can find the module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from my_son.server import app

def start_server():
    """
    Starts the FastAPI server in a background thread.
    """
    # We need to run uvicorn programmatically
    # Note: reload=False because we are in a thread
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def main():
    """
    Starts the Desktop Application.
    """
    # 1. Start Server
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # Give it a second to warm up
    time.sleep(2)

    # 2. Open Window (Launcher/Setup first)
    webview.create_window("My Son: Sovereign AGI", "http://127.0.0.1:8000/setup", width=1200, height=800, background_color='#0d1117')
    webview.start(debug=True)

if __name__ == '__main__':
    main()
