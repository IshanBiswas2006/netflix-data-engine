# Multi-stage / Production Lean Python Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install system dependencies if required (clean cache after)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY config/ ./config/
COPY data/ ./data/
COPY sql/ ./sql/
COPY src/ ./src/
COPY static/ ./static/
COPY templates/ ./templates/
COPY app.py .

# Create non-root system user for security
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose production port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Launch production WSGI Gunicorn server
CMD ["gunicorn", "--workers=2", "--threads=4", "--timeout=60", "--bind=0.0.0.0:5000", "app:app"]
