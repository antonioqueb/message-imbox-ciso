FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the SQLite database file exists
RUN mkdir -p /app/instance
RUN touch /app/instance/messages.db

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose the port
EXPOSE 5000

# Initialize the database and apply migrations
RUN flask db init || echo "Migrations already initialized"
RUN flask db migrate -m "Initial migration"
RUN flask db upgrade

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
