# Use the official Python slim image, native ARM64 for M4 processors
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS-level dependencies (useful for some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the image
COPY app/ .

# Expose Streamlit default port
EXPOSE 8501

# Add a healthcheck for Docker Compose
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start Streamlit
# We bind to 0.0.0.0 so it is accessible outside the container
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
