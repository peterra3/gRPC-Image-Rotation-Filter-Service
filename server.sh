#!/bin/bash
# server.py wrapper
# Usage: ./server.sh --port <port> --host <host>

# Directly pass command-line arguments to python script
python3 -m src.server.server "$@"