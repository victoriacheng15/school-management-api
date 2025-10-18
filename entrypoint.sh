#!/bin/sh

# Force production environment for Azure deployments
# Check if we're running in Azure Web App or if FLASK_ENV is explicitly set to production
if [ "$WEBSITE_SITE_NAME" != "" ] || [ "$FLASK_ENV" = "production" ]; then
  export FLASK_ENV=production
  echo "Production environment detected. Skipping database initialization."
else
  export FLASK_ENV=development
  echo "Development environment detected. Initializing local database..."
  echo "Waiting for PostgreSQL to be available..."
  until python3 -c "import socket; socket.create_connection(('postgres', 5432), timeout=1)" 2>/dev/null; do
      echo "PostgreSQL is unavailable - sleeping"
      sleep 2
  done
  echo "PostgreSQL is up - initializing database..."
  python3 db/init.py
fi

# Start the Flask application using Gunicorn
echo "Starting Flask application..."
exec gunicorn --workers 1 --bind 0.0.0.0:5000 run:app
