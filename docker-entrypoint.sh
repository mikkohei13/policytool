#!/bin/bash

cd dissco

# Wait for database to be ready (if using PostgreSQL)
# while ! nc -z db 5432; do sleep 1; done

# Run migrations
python manage.py migrate

# Load fixtures
python manage.py loaddata policy/fixtures/elvis/**/*.yaml common/fixtures/**/*.yaml

# Start server
python manage.py runserver 0.0.0.0:5000 