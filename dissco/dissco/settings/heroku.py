import os

import dj_database_url

from .base import *

# this is set in the heroku config vars
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [".herokuapp.com"]

DEBUG = False

MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# redirect http -> https
MIDDLEWARE.insert(1, 'django.middleware.security.SecurityMiddleware')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# allow cross-origin so that we can run the vite server on a different port but still get to the API
CORS_ALLOW_ALL_ORIGINS = True

# pull the db config from env and apply
db_from_env = dj_database_url.config(conn_max_age=60)
DATABASES['default'].update(db_from_env)
