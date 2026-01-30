import uvicorn
import os
import sys

def main():
    """
    Entry point for the My Son Agent Web Server.
    """
    # Ensure project root is in sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # Inject PYTHONPATH for subprocesses
    os.environ["PYTHONPATH"] = current_dir + os.pathsep + os.environ.get("PYTHONPATH", "")

    print("Starting My Son Agent Server...")

    # Run Uvicorn with explicit app_dir to fix Windows reload issues
    uvicorn.run(
        "my_son.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        app_dir=current_dir # CRITICAL FIX for Windows/Uvicorn import errors
    )

if __name__ == "__main__":
    main()
