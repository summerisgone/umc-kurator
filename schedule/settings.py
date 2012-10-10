# -*- coding: utf-8 -*-
import os
gettext_noop = lambda s: s
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('webmaster', 'summer.is.gone@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'schedule.sqlite'),
    }
}

TIME_ZONE = None

LANGUAGE_CODE = 'ru'

SITE_ID = 1
EMAIL_SUBJECT_PREFIX = '[schedule]'
DEFAULT_FROM_EMAIL = 'noreply@umc74.ru'
SERVER_EMAIL = 'schedule'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
#USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
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

# Don't share this with anybody.
SECRET_KEY = '5*4t-)j*3b#f58svp_ukw_lc+2pm^pnb+6@$dy0%ri+m-4bnrb'

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

ROOT_URLCONF = 'schedule.urls'


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'schedule.core',
    'schedule.core.department',
    'schedule.auth',
    'schedule.crud',
    'schedule.reports',
    'zenforms',
    'djangorestframework',
    'south',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

STATICFILES_DIRS = (
    MEDIA_ROOT,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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
    'schedule.context_processors.enums.POSITIONS_DICT',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'auth.Profile'