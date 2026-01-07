# Use Python 3.9-slim for compatibility with Django 2.2
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files first for caching
COPY resume_parser/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy the entire project directories
COPY . /app

# Create directory for AI model
RUN mkdir -p /app/resume_parser/models

# Collect static files
RUN python resume_parser/manage.py collectstatic --noinput

# Run migrations
RUN python resume_parser/manage.py migrate

# Expose the application port
EXPOSE 8000

# Default command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
