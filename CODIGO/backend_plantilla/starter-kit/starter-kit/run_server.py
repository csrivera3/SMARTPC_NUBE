#!/usr/bin/env python3
import os
import sys
import subprocess

# Get host and port from environment variables
host = os.getenv("HOST", "127.0.0.1")  # Use 0.0.0.0 for Docker/Railway
port = os.getenv("PORT", "8000")
reload_mode = os.getenv("RELOAD", "true").lower() == "true"
workers = int(os.getenv("WORKERS", "1"))

# Build uvicorn command arguments
uvicorn_args = [
    sys.executable, '-m', 'uvicorn',
    'app.main:app',
    '--host', host,
    '--port', str(port),
]

# Add reload flag for development
if reload_mode:
    uvicorn_args.append('--reload')

# Add workers for production (if > 1)
if workers > 1:
    uvicorn_args.extend(['--workers', str(workers)])

# Run uvicorn
print(f"Starting Uvicorn server on {host}:{port}")
print(f"Reload mode: {reload_mode}, Workers: {workers}")
subprocess.run(uvicorn_args)

