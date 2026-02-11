#!/usr/bin/env python3
"""
Railway startup script with proper PORT handling and error recovery
"""
import os
import sys
import subprocess
import time
import threading

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
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Start keepalive in background thread
def run_keepalive():
    """Run keepalive script in background"""
    time.sleep(30)  # Wait 30s for server to start
    try:
        subprocess.run([sys.executable, "keepalive.py"])
    except Exception as e:
        print(f"Keepalive error: {e}")

keepalive_thread = threading.Thread(target=run_keepalive, daemon=True)
keepalive_thread.start()
print("✅ Keepalive thread started")

# Start uvicorn with better error handling
try:
    subprocess.run([
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(port_int),
        "--log-level", "info",
        "--access-log"
    ], check=True)
except KeyboardInterrupt:
    print("\nShutting down gracefully...")
    sys.exit(0)
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)
