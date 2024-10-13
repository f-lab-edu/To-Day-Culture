# Base image
FROM python:3.10

# Create a non-root user and set permissions
RUN useradd -m appuser

# Set the working directory
WORKDIR /app

# Change ownership of the working directory to the non-root user
RUN chown -R appuser /app

# Set PYTHONPATH to ensure app is included in the path
ENV PYTHONPATH=/app

# Copy only requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app

# Copy Alembic directory and related files
COPY alembic/ ./alembic
COPY alembic.ini ./

# Copy tests directory (optional, if you want to run tests in the container)
COPY tests/ ./tests

# Expose the port for content-service (8000)
EXPOSE 8000

# Switch to the non-root user
USER appuser

# Run Alembic migrations before starting the app
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
