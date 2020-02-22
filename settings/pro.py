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

DEBUG = False
ALLOWED_HOSTS = ['*']


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': MYSQL_NAME,  # Or path to database file if using sqlite3.
            'USER': MYSQL_USER,  # Not used with sqlite3.
            'PASSWORD': MYSQL_PASSWORD,  # Not used with sqlite3.
            'HOST': MYSQL_HOST,  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': MYSQL_PORT,  # Set to empty string for default. Not used with sqlite3.
        }
}

if REDIS_PASSWORD:
    CELERY_BROKER_URL = 'redis://:{}@{}:{}/1'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)
else:
    CELERY_BROKER_URL = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(pathname)s process-%(process)d thread-%(thread)d %(lineno)d [%(levelname)s]: %(message)s',
            },
        },
        'handlers': {
            'file_handler': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': HOMEPATH + '/loonflow.log',
                'formatter': 'standard'
            },
            # 'console': {
            #     'level': 'DEBUG',
            #     'filters': ['require_debug_true'],
            #     'class': 'logging.StreamHandler',
            #     'formatter': 'standard'
            # },
        },
        'loggers': {
            'django': {
                'handlers': ['file_handler'],
                'propagate': True,
                'level': 'INFO',
                        },
        }
    }