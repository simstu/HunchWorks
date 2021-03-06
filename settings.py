#!/usr/bin/env python

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

# Default to debug mode, but allow it to be disabled by the environment.
DEBUG = (os.environ.get("HUNCHWORKS_DEBUG", "TRUE").upper() == "TRUE")
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": PROJECT_ROOT + "/db/development.sqlite3"
  }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Override LANGUAGES to set
#LANGUAGES = (
#  ('en', gettext_noop('English')),
#  ('es', gettext_noop('Spanish'))
#  ('fr', gettext_noop('French')),
#  ('de', gettext_noop('German')),
#  ('zh-cn', gettext_noop('Simplified Chinese')),
#  )

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# By default redirect to login page if user not authenticated
LOGIN_URL          = "/login"
LOGIN_ERROR_URL    = "/login/error/"
LOGIN_REDIRECT_URL = "/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/tmp/hunchworks/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'hunchworks/static/media')
MEDIA_URL = '/static/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%s/static' % PROJECT_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  #'django.contrib.staticfiles.finders.DefaultStorageFinder',
  'compressor.finders.CompressorFinder'
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.contrib.messages.context_processors.messages",

  # for pagination(?):
  "django.core.context_processors.request",

  # for social_auth:
  "social_auth.context_processors.social_auth_by_type_backends"
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

TEMPLATE_DIRS = (
  '%s/hunchworks/templates' % PROJECT_ROOT,
)

INSTALLED_APPS = (
  'django.contrib.contenttypes',
  'django.contrib.staticfiles',
  'django.contrib.auth',
  'django.contrib.markup',
  'activelink',
  'compressor',
  'djembedly',
  'djtokeninput',
  "social_auth",
  'hunchworks')

# In DEBUG mode, enable the Django admin.
if DEBUG:
  INSTALLED_APPS += (
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin')

# Dump logs to the console, for now.
LOGGING = {
  "version": 1,

  "handlers": {
    "console": {
      "level": "INFO",
      "class": "logging.StreamHandler"
    }
  },

  "loggers": {
    "django": {
      "handlers": ["console"],
      "level": "INFO"
    },
  }
}

CACHES = {
  "default": {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": "%s/cache" % PROJECT_ROOT
  }
}

EMBED_PROCESSORS = [
  "hunchworks.embeds.worldbank",
  "djembedly.embeds.embedly",
  "djembedly.embeds.url2png"
]

AUTH_PROFILE_MODULE = 'hunchworks.UserProfile'

COMPRESS_CSS_FILTERS = (
  "compressor.filters.css_default.CssAbsoluteFilter",
  "compressor.filters.cssmin.CSSMinFilter"
)

# Allow the scss command to be overriden by the environment. (On the staging
# server, we are running SCSS via an RVM gemset wrapper in /usr/local/bin.)
SCSS_CMD = os.environ.get("HUNCHWORKS_SCSS", "scss")

COMPRESS_PRECOMPILERS = (
  ("text/x-scss", "%s {infile} {outfile}" % SCSS_CMD),
)

AUTHENTICATION_BACKENDS = (
  "social_auth.backends.twitter.TwitterBackend",
  "social_auth.backends.facebook.FacebookBackend",
  "social_auth.backends.google.GoogleOAuthBackend",
  "social_auth.backends.google.GoogleOAuth2Backend",
  "social_auth.backends.google.GoogleBackend",
  "social_auth.backends.yahoo.YahooBackend",
  "social_auth.backends.contrib.linkedin.LinkedinBackend",
  "social_auth.backends.contrib.livejournal.LiveJournalBackend",
  "social_auth.backends.contrib.orkut.OrkutBackend",
  "social_auth.backends.contrib.foursquare.FoursquareBackend",
  "social_auth.backends.contrib.github.GithubBackend",
  "social_auth.backends.contrib.dropbox.DropboxBackend",
  "social_auth.backends.contrib.flickr.FlickrBackend",
  "social_auth.backends.OpenIDBackend",
  "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_ENABLED_BACKENDS = ("twitter", "google", "linkedin", "facebook")
SOCIAL_AUTH_ERROR_KEY = "social_errors"

GOOGLE_DISPLAY_NAME = "HunchWorks"

try: from keys import *
except ImportError: pass
