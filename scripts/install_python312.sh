#!/bin/bash

# Script to install Python 3.12 on Ubuntu
# This script handles apt_pkg issues and installs Python 3.12 from deadsnakes PPA

set -e

echo "=== Python 3.12 Installation Script ==="
echo ""

# Fix apt_pkg issues first
echo "[Step 1/5] Fixing apt_pkg module issues..."
sudo apt remove --purge command-not-found -y 2>/dev/null || true
sudo apt --fix-broken install -y 2>/dev/null || true

# Update package list
echo "[Step 2/5] Updating package list..."
sudo apt update

# Install software-properties-common if not present
echo "[Step 3/5] Installing prerequisites..."
sudo apt install -y software-properties-common

# Add deadsnakes PPA
echo "[Step 4/5] Adding deadsnakes PPA for Python 3.12..."
sudo add-apt-repository ppa:deadsnakes/ppa -y

# Update again after adding PPA
sudo apt update

# Install Python 3.12
echo "[Step 5/5] Installing Python 3.12 and related packages..."
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Note: python3.12-distutils is not available, pip can be installed via get-pip.py if needed

echo ""
echo "=== Verifying Python 3.12 installation ==="
python3.12 --version

echo ""
echo "=== Available Python versions on your system ==="
ls -1 /usr/bin/python3.* 2>/dev/null | grep -E "python3\.[0-9]+$" | while read pybin; do
    echo -n "$pybin: "
    $pybin --version 2>/dev/null || echo "not working"
done

echo ""
echo "=== Creating Python 3.12 virtual environment ==="
cd /home/aiyrh/git/PythonRuns
python3.12 -m venv .venv312
echo "Virtual environment created at: /home/aiyrh/git/PythonRuns/.venv312"

echo ""
echo "=== Installing pip in the virtual environment ==="
.venv312/bin/python -m ensurepip --upgrade
.venv312/bin/pip install --upgrade pip setuptools wheel

echo ""
echo "✅ Python 3.12 installation complete!"
echo ""
echo "To use Python 3.12, run:"
echo "  cd /home/aiyrh/git/PythonRuns"
echo "  source .venv312/bin/activate"
echo "  pip install -r requirements.txt"
echo ""

