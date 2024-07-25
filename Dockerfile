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

# Initialize the database (this will run on container start)
CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0"]
