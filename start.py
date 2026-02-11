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
    time.sleep(60)  # Wait 60s for server to fully start
    while True:
        try:
            subprocess.run([sys.executable, "keepalive.py"])
        except Exception as e:
            print(f"Keepalive error: {e}, restarting in 10s...")
            time.sleep(10)

keepalive_thread = threading.Thread(target=run_keepalive, daemon=True)
keepalive_thread.start()
print("✅ Keepalive thread started (will begin in 60s)")

# Start uvicorn with auto-restart on failure
max_retries = 5
retry_count = 0

while retry_count < max_retries:
    try:
        print(f"🚀 Starting uvicorn server (attempt {retry_count + 1}/{max_retries})...")
        result = subprocess.run([
            "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", str(port_int),
            "--log-level", "info",
            "--access-log"
        ])
        
        # If server exits cleanly (exit code 0), don't retry
        if result.returncode == 0:
            print("Server shut down cleanly")
            break
        
        # Server crashed, increment retry counter
        retry_count += 1
        if retry_count < max_retries:
            print(f"⚠️ Server crashed with exit code {result.returncode}, restarting in 5s...")
            time.sleep(5)
        else:
            print(f"❌ Max retries ({max_retries}) reached, giving up")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        retry_count += 1
        if retry_count < max_retries:
            print(f"Retrying in 5s... ({retry_count}/{max_retries})")
            time.sleep(5)
        else:
            print(f"❌ Max retries ({max_retries}) reached")
            sys.exit(1)

print("Server process ended")
