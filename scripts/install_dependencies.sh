#!/bin/bash

# Script to install PythonRuns dependencies using pip (setuptools approach)
# This is the recommended approach since the project uses setuptools, not Poetry

set -e

echo "=== PythonRuns Dependency Installation Script ==="
echo ""

# Check if we're in the correct directory
cd /home/aiyrh/git/PythonRuns

# Determine which virtual environment to use
if [ -d ".venv312" ]; then
    VENV_PATH=".venv312"
    echo "Using Python 3.12 virtual environment (.venv312)"
elif [ -d ".venv" ]; then
    VENV_PATH=".venv"
    echo "Using Python 3.11 virtual environment (.venv)"
else
    echo "Error: No virtual environment found. Please create one first."
    exit 1
fi

echo ""
echo "[Step 1/4] Activating virtual environment..."
source $VENV_PATH/bin/activate

echo ""
echo "[Step 2/4] Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

echo ""
echo "[Step 3/4] Installing project in editable mode with dependencies..."
pip install -e .

echo ""
echo "[Step 4/4] Verifying key packages are installed..."
echo ""
echo "Checking installed packages:"
pip list | grep -E "(numpy|jax|mediapipe|python-jose|pytest)" || echo "Some packages may not be installed yet"

echo ""
echo "=== Testing JWT module ==="
python sources/jwt_test.py

echo ""
echo "✅ Installation complete!"
echo ""
echo "Your project is now set up using pip + setuptools."
echo ""
echo "To activate the environment in the future, run:"
echo "  cd /home/aiyrh/git/PythonRuns"
echo "  source $VENV_PATH/bin/activate"
echo ""

