#!/usr/bin/env bash
set -e
export PYTHONPATH=/app

echo "Waiting for DB to start..."
sleep 1

echo "Seeding the database..."
python data/seed_data.py

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
