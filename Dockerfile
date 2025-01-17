FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including PostgreSQL dev files
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY setup.py setup.cfg pyproject.toml ./
COPY README.md ./
COPY dissco ./dissco

RUN pip install -e .[test]

# Run migrations and load fixtures on container startup
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/docker-entrypoint.sh"] 