#!/bin/sh

# Run database initialization
echo "Initializing the database..."
python3 db/init_db.py

# Populate the database with data
echo "Populating the database..."
python3 db/populate_db.py

sleep 5

# Start the Flask application using Gunicorn
echo "Starting Flask application..."
exec gunicorn --bind 0.0.0.0:5000 app:app
