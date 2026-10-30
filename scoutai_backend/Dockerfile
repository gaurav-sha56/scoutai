# Multi-stage / optimized slim build for CrewAI FastAPI backend
FROM python:3.12-slim

# Prevent Python buffering and bytecode generation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PORT=8000 \
    HOME="/home/appuser"

# Install minimal system dependencies for networking and health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv from official binary image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a dedicated non-root user and group
RUN useradd -m -u 1000 -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy dependency configuration files first for Docker layer caching
COPY pyproject.toml uv.lock ./

# Install project dependencies into virtual environment (.venv)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source code
COPY src/ ./src/

# Install the application package
RUN uv sync --frozen --no-dev

# Set ownership of /app to non-root user
RUN chown -R appuser:appuser /app /home/appuser

# Add virtual environment binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose FastAPI server port
EXPOSE 8000

# Container health check using FastAPI /docs endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/docs || exit 1

# Default command: Start FastAPI with Uvicorn using the environment PORT or default to 8000
CMD ["sh", "-c", "exec uvicorn scoutai_backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
