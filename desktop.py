import sys
import threading
import time
import socket
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

def wait_for_server(host, port, timeout=10):
    """
    Waits for the server to be available.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(0.2)
    return False

def main():
    """
    Starts the Desktop Application.
    """
    # 1. Start Server
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # 2. Wait for Server
    if wait_for_server("127.0.0.1", 8000):
        start_url = "http://127.0.0.1:8000/setup"
    else:
        # Fallback if server fails (e.g. port blocked)
        # We can try to serve a static error or just point to it and let webview show error
        start_url = "http://127.0.0.1:8000/setup"
        print("Warning: Server start timed out.")

    # 3. Open Window (Launcher/Setup first)
    webview.create_window("Autonomous Agent", start_url, width=1200, height=800, background_color='#0d1117')
    webview.start(debug=True)

if __name__ == '__main__':
    main()
