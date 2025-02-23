FROM python:3.11.6-slim

# Instalar dependencias del sistema y git
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Instalar herramientas de desarrollo
RUN pip install fastapi uvicorn pytest black flake8 sqlalchemy psycopg2-binary
