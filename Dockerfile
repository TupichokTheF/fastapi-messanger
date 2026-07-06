FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
RUN uv sync --frozen --no-cache --no-dev --no-install-project

COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "app.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]