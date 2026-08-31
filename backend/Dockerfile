# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# psycopg (pure-Python build, no [binary] extra) loads libpq at runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

# uv, copied from its official image (see https://docs.astral.sh/uv/guides/integration/docker/)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install only the backend's own deps - the "backend" extra excludes PySide6/Qt
# entirely, so this image doesn't pay for GUI dependencies it never uses.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --extra backend

# Only the code the backend actually needs
COPY backend/ ./backend/
COPY database/ ./database/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
