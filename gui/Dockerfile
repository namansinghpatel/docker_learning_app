# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    QT_QPA_PLATFORM=xcb \
    QT_X11_NO_MITSHM=1

WORKDIR /app

# Runtime libraries PySide6/Qt needs to import and to open an X11 window
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgl1 \
        libegl1 \
        libopengl0 \
        libxkbcommon0 \
        libxkbcommon-x11-0 \
        libdbus-1-3 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xinerama0 \
        libxcb-xfixes0 \
        libfontconfig1 \
        libfreetype6 \
        libxrender1 \
        libxi6 \
        libsm6 \
        libice6 \
        libxext6 \
        libnss3 \
        libnspr4 \
        libcups2 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install only the GUI's own deps - the "gui" extra excludes FastAPI/psycopg/
# uvicorn entirely, so this image never carries a backend it doesn't run.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --extra gui

COPY gui/ ./gui/

CMD ["uv", "run", "python", "gui/main.py"]
