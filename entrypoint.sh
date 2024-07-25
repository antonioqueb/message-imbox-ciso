#!/bin/sh

# Check if the database file exists
if [ ! -f "/app/instance/messages.db" ]; then
  echo "Database not found. Initializing database..."
  flask db init || echo "Migrations already initialized"
  flask db migrate -m "Initial migration"
  flask db upgrade
else
  echo "Database found. Skipping initialization."
fi

# Always apply the latest migrations
flask db upgrade

# Run the application
flask run --host=0.0.0.0
