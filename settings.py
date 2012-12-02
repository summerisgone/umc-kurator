# Django settings for kurator project.
import os
import dj_database_url

gettext_noop = lambda s: s
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = 'DEBUG' in os.environ
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('webmaster', 'summer.is.gone@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {}

config = dj_database_url.config()
if config:
    DATABASES['default'] = config
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': os.path.join(PROJECT_DIR, 'kurator.sqlite'),
        'NAME': 'kurator',
    }

TIME_ZONE = None

LANGUAGE_CODE = 'ru'

SITE_ID = 1

EMAIL_SUBJECT_PREFIX = '[kurator]'
DEFAULT_FROM_EMAIL = 'noreply@umc74.ru'
SERVER_EMAIL = 'kurator'

USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'upload')
UPLOAD_DIR = 'upload'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
UPLOAD_URL = MEDIA_URL + UPLOAD_DIR

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


# Additional locations of static files
STATICFILES_DIRS = (
    MEDIA_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5*4t-)j*3b#f58svp_ukw_lc+2pm^pnb+6@$dy0%ri+m-4bnrb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'staticfiles.context_processors.static',
    'context_processors.enums.LISTENER_POSITIONS',
    'context_processors.get_params',
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.messages',
    'core',
    'core.department',
    'core.manager',
    'core.auth',

    'crud',
    'reports',

    'staticfiles',
    'zenforms',
    'djangorestframework',
    'south',
    'celery',
    'djcelery',
    'storages',
    'compressor',
    'gunicorn',
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Static S3 settings
if 'AWS_ACCESS_KEY_ID' in os.environ:
    S3_STORAGE = 'storage.CachedS3BotoStorage'
    AWS_STORAGE_BUCKET_NAME = 'umc_kurator'

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    if not DEBUG:
        STATICFILES_STORAGE = S3_STORAGE
        STATIC_URL = 'http://umc_kurator.s3.amazonaws.com/'
        ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

        COMPRESS_STORAGE = S3_STORAGE
        COMPRESS_OFFLINE = True
        COMPRESS_URL = STATIC_URL

# Hope, temporary
COMPRESS_ENABLED = False

# Setup Email from mailgun

if 'MAILGUN_SMTP_SERVER' in os.environ:
    EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
    EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
    EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
    EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']


# Setup DEBUG mode
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
#    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ('127.0.0.1',)
