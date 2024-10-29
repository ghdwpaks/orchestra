# local.py

from .base import *

DEBUG = True
SECRET_KEY = 'your-local-secret-key'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
