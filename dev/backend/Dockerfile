FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . ./backend

# Set the environment variable to ensure Python can find the 'backend' package
ENV PYTHONPATH=/app

# Start the application using the package path.
# In a multi-instance setup, we typically use uvicorn or gunicorn.
# We keep it simple with uvicorn here, but pointing to the module correctly.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
