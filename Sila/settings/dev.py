from os.path import abspath, dirname, join
from .base import TEMPLATES, INSTALLED_APPS, DOMAIN_DEVELOPMENT, ADMINS
from .production import DATABASES

ENVIRONMENT = 'DEV'
DEBUG = False
COMPRESS_OFFLINE = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

INSTALLED_APPS += (
    # 'debug_toolbar',
)

# INTERNAL_IPS = ('127.0.0.1', '0.0.0.0',)

ALLOWED_HOSTS = DOMAIN_DEVELOPMENT

STATIC_ROOT = '/home/sila/static/'
MEDIA_ROOT = '/home/sila/media/'


SECRET_KEY = '7nn(g(lb*8!r_+cc3m8bjxm#xu!q)6fidwgg&$p$6a+alm+x'

# Use Dummy cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'