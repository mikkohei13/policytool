import os

import dj_database_url

from .base import *

# this is set in the heroku config vars
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = True

MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# allow cross-origin so that we can run the vite server on a different port but still get to the API
CORS_ALLOW_ALL_ORIGINS = True

# pull the db config from env and apply
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
