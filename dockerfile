FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Install immich-face-to-album package
RUN pip install --no-cache-dir immich-face-to-album schedule

# Copy application files
COPY app/ .

# Create non-root user
RUN useradd -m -u 1000 immich && \
    chown -R immich:immich /app
USER immich

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('${IMMICH_SERVER}/api/server-info')" || exit 1

# Run the application
CMD ["python", "main.py"]