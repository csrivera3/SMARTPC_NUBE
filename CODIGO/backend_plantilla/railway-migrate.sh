#!/bin/bash
# Railway Migrations Runner
# This script should be executed as a one-time job in Railway to set up the database schema
# Usage: railway run bash railway-migrate.sh

set -e

echo "[$(date +'%Y-%m-%d %H:%M:%S')] Starting database migrations..."
echo "Database URL: $DATABASE_URL"

# Navigate to the application directory
cd /app

# Check if alembic is available
if ! command -v alembic &> /dev/null; then
    echo "[ERROR] alembic is not installed"
    exit 1
fi

# Run migrations
echo "[$(date +'%Y-%m-%d %H:%M:%S')] Running Alembic migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] SUCCESS: Database migrations completed"
    exit 0
else
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: Database migrations failed"
    exit 1
fi
