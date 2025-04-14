#!/usr/bin/env bash
set -e

echo "Waiting for Postgres to be ready..."
./wait-for-it.sh db:5432 -t 30 -- echo "Postgres is up!"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding the database..."
poetry run python app/ingestion/seed_data.py

echo "Starting the API server..."
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080