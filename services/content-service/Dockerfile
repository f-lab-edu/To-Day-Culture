# Base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy only requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application code
COPY app/ ./app
COPY alembic/ ./alembic
COPY alembic.ini .

# Expose the port for content-service (8000)
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
