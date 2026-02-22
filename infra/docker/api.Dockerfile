FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
      alembic \
      asyncpg \
      celery \
      cryptography \
      fastapi \
      httpx \
      itsdangerous \
      kubernetes \
      pydantic-settings \
      python-multipart \
      redis \
      sqlalchemy \
      uvicorn

COPY . /app

EXPOSE 8000
