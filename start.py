#!/usr/bin/env python3
"""
Railway startup script with proper PORT handling
"""
import os
import sys

# Get PORT from environment, default to 8000
port = os.environ.get("PORT", "8000")

# Validate port is a number
try:
    port_int = int(port)
    if port_int < 1 or port_int > 65535:
        print(f"Invalid port number: {port_int}")
        sys.exit(1)
except ValueError:
    print(f"PORT must be a number, got: {port}")
    sys.exit(1)

print(f"Starting Musicly Backend on port {port_int}...")

# Start uvicorn
os.execvp("uvicorn", [
    "uvicorn",
    "app.main:app",
    "--host", "0.0.0.0",
    "--port", str(port_int)
])
