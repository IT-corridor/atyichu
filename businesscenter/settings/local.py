from base import *

SECRET_KEY = 'g%vsow(2i!3k_*+o=$1rp5hm=9+ivwpqbk0grvs8=pgo=4c$vh'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static_dev'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp', 'email')
