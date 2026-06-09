#!/bin/bash
# Cross-platform launcher script for Image Editor

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Check for pre-built executable
if [ -f "$SCRIPT_DIR/dist/ImageEditor" ]; then
    echo "Launching pre-built executable..."
    "$SCRIPT_DIR/dist/ImageEditor" "$@"
    exit 0
fi

# Check for virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    python "$SCRIPT_DIR/main.py" "$@"
    exit 0
fi

# Fallback to system Python
if command -v python3.13 &> /dev/null; then
    python3.13 "$SCRIPT_DIR/main.py" "$@"
elif command -v python3 &> /dev/null; then
    python3 "$SCRIPT_DIR/main.py" "$@"
else
    echo "Error: Python 3.13+ is required but not found."
    echo "Please install Python 3.13 or use the pre-built executable."
    exit 1
fi
