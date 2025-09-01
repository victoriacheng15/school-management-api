#!/bin/sh

sleep 5

# Wait for PostgreSQL to be ready
if [ "$DATABASE_TYPE" = "postgresql" ]; then
    echo "Waiting for PostgreSQL to be available..."
    until python3 -c "import socket; socket.create_connection(('postgres', 5432), timeout=1)" 2>/dev/null; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "PostgreSQL is up - initializing database..."
    python3 db/init_postgresql.py
else
    echo "Initializing SQLite database..."
    python3 db/init_db.py
    echo "Populating the database..."
    python3 db/populate_db.py
fi

# Start the Flask application using Gunicorn
echo "Starting Flask application..."
exec gunicorn --bind 0.0.0.0:5000 run:app
