#!/bin/bash
# Start script for Railway deployment
# Ensures PORT is properly set and passed to gunicorn

PORT=${PORT:-8080}
echo "Starting server on port $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
