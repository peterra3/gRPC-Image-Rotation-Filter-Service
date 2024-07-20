#!/bin/bash
# client.py wrapper
# Usage: ./client.sh --host <host> --port <port> --input <input_file> --output <output_file> --rotate <rotation> --mean <mean_filter>

# Directly pass command-line arguments to python script
python3 -m src.client.client "$@"