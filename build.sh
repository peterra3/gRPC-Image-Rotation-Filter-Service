#!/bin/bash
# build.sh
# Builds necessary components for the gRPC server and client.

echo "Building the gRPC ImageRPC service..."

# Optional: Initialize a Python virtual environment
# python3 -m venv venv
# source venv/bin/activate

# Compile protobuf files
python3 -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./src/proto/image.proto

echo "Build completed."