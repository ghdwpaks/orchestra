# production.py

from .base import *

DEBUG = False
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['your-production-domain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB_NAME'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': '3306',
    }
}

CORS_ALLOWED_ORIGINS = [
    '15.152.30.9',
]

SECURE_SSL_REDIRECT = True  # HTTPS 강제 적용
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
