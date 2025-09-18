#!/bin/sh


# Set FLASK_ENV to production if not already set
export FLASK_ENV=production

if [ "$FLASK_ENV" = "production" ]; then
  echo "Production environment detected. Skipping database initialization."
else
  echo "Development environment detected. Initializing local database..."
  echo "Waiting for PostgreSQL to be available..."
  until python3 -c "import socket; socket.create_connection(('postgres', 5432), timeout=1)" 2>/dev/null; do
      echo "PostgreSQL is unavailable - sleeping"
      sleep 2
  done
  echo "PostgreSQL is up - initializing database..."
  python3 db/init_postgresql.py
fi

# Start the Flask application using Gunicorn
echo "Starting Flask application..."
exec gunicorn --bind 0.0.0.0:5000 run:app
