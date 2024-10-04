# Base image
FROM python:3.10

# Create a non-root user and set permissions
RUN useradd -m appuser

# Set the working directory
WORKDIR /app

# Change ownership of the working directory to the non-root user
RUN chown -R appuser /app

# Copy only requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application code
COPY app/ ./app
COPY alembic/ ./alembic
COPY alembic.ini .

# Expose the port for content-service (8000)
EXPOSE 8000

# Switch to the non-root user
USER appuser

# Run the app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
