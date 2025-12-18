import uvicorn
import os
import sys

def main():
    """
    Entry point for the My Son Agent Web Server.
    """
    # Ensure project root is in sys.path for subprocesses (uvicorn reload)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # Also inject PYTHONPATH environment variable for subprocesses
    os.environ["PYTHONPATH"] = current_dir + os.pathsep + os.environ.get("PYTHONPATH", "")

    print("Starting My Son Agent Server...")

    # Run the Uvicorn server
    # The app is defined in my_son.server:app
    uvicorn.run("my_son.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
