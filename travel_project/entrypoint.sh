#!/bin/bash

# Wait for the PostgreSQL database to be ready
./wait-for-it.sh postgres:5432 --timeout=30 --strict -- echo "Postgres is up and running"

# Check if the migrations have already been applied
if [ ! -f /usr/src/app/migrations_applied ]; then
    echo "Applying database migrations..."
    python manage.py makemigrations
    python manage.py migrate
    touch /usr/src/app/migrations_applied
    echo "Migrations applied."
else
    echo "Migrations have already been applied."
fi

# Run the application
exec "$@"
