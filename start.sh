#!/bin/bash
# Railway startup script with proper PORT handling

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting Musicly Backend on port $PORT..."

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
