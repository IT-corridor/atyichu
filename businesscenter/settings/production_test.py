import os
import json
from .base import *
from .mailgun import *

config_path = os.path.join(BASE_DIR, 'config.json')
with open(config_path, 'r') as f:
    data = json.load(f)
SECRET_KEY = data['SECRET_KEY']

# RESOURCE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'a-static')

DEBUG = False

ALLOWED_HOSTS = ['.atyichu.com']
USE_X_FORWARDED_HOST = True
ADMINS = ((data['ADMIN'], data['ADMIN_EMAIL']),)   # hide


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# NEED to set a user and a password before deployment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': data['DB_NAME'],
        'USER': data['DB_USER'],
        'PASSWORD': data['DB_PASSWORD'],
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


EMAIL_BACKEND = 'django_mailgun_mime.backends.MailgunMIMEBackend'
MAILGUN_API_KEY = data['MAILGUN_API_KEY']
MAILGUN_DOMAIN_NAME = data['MAILGUN_DOMAIN_NAME']

DEFAULT_FROM_EMAIL = 'post@atyichu.com'
SERVER_EMAIL = 'beholder@atyichu.com'

WEIXIN_APP_ID = data['WEIXIN_APP_ID']
WEIXIN_SECRET = data['WEIXIN_SECRET']

