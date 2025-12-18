#!/bin/bash
echo "Initializing My Son (Global Mode)..."

# Install Deps Globally
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run
echo "Starting Agent..."
python3 main.py
