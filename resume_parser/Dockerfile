# Use specific python version for reproducibility and slim for size
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore
ENV DJANGO_SETTINGS_MODULE resume_parser.settings

# Set work directory
WORKDIR /app

# Install system dependencies
# build-essential: for compiling python packages
# cmake: for llama-cpp-python
# git: for some pip installs if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libopenblas-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

# Upgrade pip and build tools to prevent compilation errors
RUN pip install --upgrade pip setuptools wheel

# Install CPU-only PyTorch first to avoid downloading huge CUDA/Nvidia packages
# We match the version from requirements.txt (2.2.2)
RUN pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu

# Install generic requirements
RUN pip install --no-cache-dir -r requirements.txt

# Re-install llama-cpp-python with OpenBLAS support for faster inference
# We need to force reinstall to trigger compilation with the new CMAKE args
RUN CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_OPENBLAS=ON" pip install llama-cpp-python==0.3.16 --force-reinstall --upgrade --no-cache-dir

# Force reinstall numpy to ensure binary compatibility and verify it works
RUN pip install --force-reinstall --no-cache-dir numpy==1.26.4
RUN python -c "import numpy; print(f'Numpy {numpy.__version__} works')"

# Copy download script and download models
# This uses the docker cache effectively - if requirements don't change, 
# we don't re-download models unless the script changes
COPY scripts/download_models.py ./scripts/
RUN python scripts/download_models.py

# Copy project
COPY . .

# Run migrations and collect static (for sqlite based setup)
# Note: For production with external DB, migrations should be run at runtime
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate

# Expose port
EXPOSE 8000

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]