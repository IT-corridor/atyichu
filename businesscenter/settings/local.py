from .base import *

SECRET_KEY = 'g%vsow(2i!3k_*+o=$1rp5hm=9+ivwpqbk0grvs8=pgo=4c$vh'
DEBUG = True
ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-US'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
        }
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_dev')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp', 'email')

WEIXIN_APP_ID = ''
WEIXIN_SECRET = ''
