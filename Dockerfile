# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.14-alpine3.23 AS builder

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-cache --no-group dev --no-install-project

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM python:3.14-alpine3.23 AS runner

WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code with correct ownership
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup pyproject.toml ./

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

# Document exposed port
EXPOSE 8000

# Run with uvicorn
ENTRYPOINT ["uvicorn"]
CMD ["fastapi_template.main:app", "--host", "0.0.0.0", "--port", "8000"]