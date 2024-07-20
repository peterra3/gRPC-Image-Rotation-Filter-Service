#!/bin/bash
# setup.sh
# Installs dependencies and sets up the system for the ImageRPC server and client.

echo "Setting up the environment for the gRPC ImageRPC service..."

# Update package lists
sudo apt-get update

# Install Python and pip (specify Python version if needed, e.g., python3.8)
sudo apt-get install -y python3 python3-pip

echo "Installing Python packages from requirements.txt..."
pip3 install -r requirements.txt

echo "Setup completed."