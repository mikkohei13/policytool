#!/bin/bash

cd dissco

# Wait for database to be ready
while ! nc -z db 5432; do
    echo "Waiting for postgres..."
    sleep 1
done
echo "PostgreSQL started"

# Set Django settings module to docker
export DJANGO_SETTINGS_MODULE=dissco.settings.docker

# Run migrations
python manage.py migrate

# Load fixtures
python manage.py loaddata policy/fixtures/elvis/**/*.yaml common/fixtures/**/*.yaml

# Start server
python manage.py runserver 0.0.0.0:5000 