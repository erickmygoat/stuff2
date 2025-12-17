import uvicorn
import os

def main():
    """
    Entry point for the My Son Agent Web Server.
    """
    print("Starting My Son Agent Server...")

    # Run the Uvicorn server
    # The app is defined in my_son.server:app
    uvicorn.run("my_son.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
