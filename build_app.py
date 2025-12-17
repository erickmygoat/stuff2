"""
Script to build the standalone executable.
"""
import PyInstaller.__main__
import os
import shutil

def build():
    print("Building My Son standalone application...")

    # Define hidden imports required for complex libraries
    hidden_imports = [
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'llama_cpp',
        'chromadb',
        'chromadb.telemetry.product.posthog',
        # Add other specific submodules if runtime errors occur
    ]

    args = [
        'main.py',
        '--name=MySon',
        '--onefile',
        '--clean',
        '--add-data=templates:templates', # Include HTML templates
        '--add-data=models:models',       # Include the brain (if present)
    ]

    for imp in hidden_imports:
        args.append(f'--hidden-import={imp}')

    # Run PyInstaller
    PyInstaller.__main__.run(args)

    print("Build complete. Executable is in 'dist/'.")

if __name__ == "__main__":
    build()
