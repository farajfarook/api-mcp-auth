# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration files
COPY MCPProxy/pyproject.toml .
COPY MCPProxy/uv.lock* ./

# Install uv for faster package management
RUN pip install uv

# Install Python dependencies using uv sync for reproducible builds
RUN uv sync --frozen --no-dev

# Copy the application code
COPY MCPProxy/shared/ ./shared/
COPY MCPProxy/fastapimcp_server_oauth.py .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose the port the app runs on
EXPOSE 8009

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8009/api/public')" || exit 1

# Command to run the application
CMD ["python", "-m", "uvicorn", "fastapimcp_server_oauth:app", "--host", "0.0.0.0", "--port", "8009"]
