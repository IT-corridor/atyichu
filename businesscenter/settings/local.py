from .base import *

SECRET_KEY = 'g%vsow(2i!3k_*+o=$1rp5hm=9+ivwpqbk0grvs8=pgo=4c$vh'
DEBUG = True
ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-US'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_orig.sqlite3'),

    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_dev')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp', 'email')

WEIXIN_APP_ID = 'wx923ca88a0f604e90'
WEIXIN_SECRET = '392aad4be93c5bf2a535d5b932186b7b'
WEIXIN_QR_APP_ID = 'wx6ad4cd8923e9ea5e'
WEIXIN_QR_SECRET = 'a385ba5adf67452659c3ff7615e86198'

IMAGGA_KEY = ''
IMAGGA_SECRET = ''
IMAGGA_LANG = 'zh_chs'
