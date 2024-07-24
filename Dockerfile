FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear el directorio instance
RUN mkdir -p /app/instance

# Crear el archivo app.db
RUN touch /app/instance/app.db

CMD ["python", "app.py"]
