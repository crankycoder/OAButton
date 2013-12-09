# Django settings for oabutton project.

from os.path import dirname, abspath, join
import time

ROOT_PATH = dirname(dirname(abspath(__file__)))
STATIC_PUBLIC = join(ROOT_PATH, 'oabutton', 'static', 'public')

# Get the deployed version from VERSION_FILE or fall back to unknown
VERSION_FILE = join(STATIC_PUBLIC, 'version.txt')
try:
    with open(VERSION_FILE) as f:
        VERSION = f.read().strip()
except IOError:
    VERSION = time.time()

# Start override vars #
DEBUG = True
TEMPLATE_DEBUG = DEBUG
HOSTNAME = 'http://localhost:8000'
# End override vars

try:
    from settings_local import *   # NOQA
except:
    print "Can't load settings_local - CORE won't work"


ADMINS = (
    ('Victor Ng', 'victor@crankycoder.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Toronto'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# These are the only two thigns you need for static file loading
# in a dev enviroment
STATIC_URL = '/static/'
STATICFILES_DIRS = (STATIC_PUBLIC,)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# We don't use any regular security bits, so just make up some random
# security key thing
import hashlib
import random
SECRET_KEY = hashlib.sha256("%x" % random.getrandbits(60 * 8)).hexdigest()

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'oabutton.middleware.StaticCacheBuster',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'oabutton.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'oabutton.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "oabutton.context_processors.version"
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [
    'django.contrib.auth',

    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.admin',

    # The bookmarklet app is both the web interface and the API
    # break it out into a proper API section
    'oabutton.apps.bookmarklet',

    # The web app is the main website
    'oabutton.apps.web',

    # This is for CORE. I think.  bah.
    'oabutton.apps.metadata',

    # Our new API interface
    'oabutton.apps.api',


    # Our new API interface
    'oabutton.apps.quickstart',

    'south',

    'rest_framework',
]

if DEBUG:
    INSTALLED_APPS.append('django.contrib.staticfiles')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'oabutton.apps.metadata.views': {
            'handlers': ['console'],
            'level': 'WARN',
        },
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    # Send cookies only over HTTPS connections for production setup
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Expire cookies in 24 hours
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = False

# Use persistent sessions in the database
SESSION_ENGINE = 'django.contrib.sessions.backends.db'


# REST Framework stuff

REST_FRAMEWORK = {
        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
        'PAGINATE_BY': 10
        }
