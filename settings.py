# Django settings for kurator project.
import os
gettext_noop = lambda s: s
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('webmaster', 'summer.is.gone@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {}
try:
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()
except ImportError:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'schedule.sqlite'),
    }

TIME_ZONE = None

LANGUAGE_CODE = 'ru'

SITE_ID = 1

EMAIL_SUBJECT_PREFIX = '[schedule]'
DEFAULT_FROM_EMAIL = 'noreply@umc74.ru'
SERVER_EMAIL = 'schedule'

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
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'context_processors.enums.LISTENER_POSITIONS',
    'context_processors.get_params',
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'core',
    'department',
    'auth',
    'crud',
    'reports',
    'zenforms',
    'djangorestframework',
    'south',
    'celery',
]

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