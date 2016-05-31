from .base import *

SECRET_KEY = 'g%vsow(2i!3k_*+o=$1rp5hm=9+ivwpqbk0grvs8=pgo=4c$vh'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'atyichu',
        'USER': 'dummy',
        'PASSWORD': 'dindOng',
        'STORAGE_ENGINE': 'MyISAM',
        'HOST': 'localhost',
        'PORT': '',
        #'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': True,

        'TEST': {
            'NAME': 'atyichu_test',
            'CHARSET': 'utf8',
            'SERIALIZE': False,

        },
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static_dev'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp', 'email')
