#!/bin/bash
# entrypoint.sh - Startup script for FastAPI application
# This script interprets environment variables and starts uvicorn

set -e

# Log startup information
echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting MesaPass API application..."

# Get environment variables with defaults
PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}
WORKERS=${WORKERS:-1}
LOG_LEVEL=${LOG_LEVEL:-info}

echo "[$(date +'%Y-%m-%d %H:%M:%S')] Configuration:"
echo "  - HOST: $HOST"
echo "  - PORT: $PORT"
echo "  - WORKERS: $WORKERS"
echo "  - LOG_LEVEL: $LOG_LEVEL"
echo "  - Environment: ${ENVIRONMENT:-development}"

# Verify PORT is a valid integer
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "[ERROR] PORT must be a valid integer, got: $PORT"
    exit 1
fi

# Start uvicorn application
echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting uvicorn..."
exec uvicorn app.main:app \
  --host "$HOST" \
  --port "$PORT" \
  --log-level "$LOG_LEVEL" \
  --proxy-headers \
  --forwarded-allow-ips='*' \
  --access-log
