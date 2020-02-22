from settings.common import *

MIDDLEWARE = [
    'service.csrf_service.DisableCSRF',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'service.permission.api_permission.ApiPermissionCheck',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''
if REDIS_PASSWORD:
    CELERY_BROKER_URL = 'redis://:{}@{}:{}/1'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)
else:
    CELERY_BROKER_URL = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)
