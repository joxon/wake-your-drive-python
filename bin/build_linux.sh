#!/bin/bash
VENV_DIR="venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing Dependencies..."
pip install -r requirements.txt

echo ""
echo "Building WakeTheDrive for Linux..."
pyinstaller --onefile --name "WakeTheDrive_Linux" ../src/__main__.py

echo ""
echo "Done! Your executable is in the 'dist' folder."
chmod +x dist/WakeTheDrive_Linux

echo "Deactivating virtual environment..."
deactivate
