import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

# RESOURCE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'a-static')

DEBUG = False

ALLOWED_HOSTS = ['.atyichu.com']
USE_X_FORWARDED_HOST = True
ADMINS = ((os.environ['ADMIN'], os.environ['ADMIN_EMAIL']),)   # hide


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# NEED to set a user and a password before deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'rm-2ze8182fmzl45fh0r.mysql.rds.aliyuncs.com',
        'PORT': 3306,
        'TEST': {
            'NAME': 'db_atyichu_test',
        }
        #'ATOMIC_REQUESTS': True,
    }
}

# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# Static files will be serving by the proxy server
# and it have to be outside of the project root

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
