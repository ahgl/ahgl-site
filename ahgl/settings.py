# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import posixpath
import djcelery

gettext = lambda s: s

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

djcelery.setup_loader()

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = True

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "dev.db",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Pacific"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"
LANGUAGES = (
    ('en', gettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "aaaa" #change this - the open source version just has something dumb

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.transaction.TransactionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "ahgl.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static",
    
    "pinax.core.context_processors.pinax_settings",
    
    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    "messages.context_processors.inbox",
    
    "pybb.context_processors.processor",
    
    "apps.tournaments.context_processors.tournaments",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    
    "pinax.templatetags",
    
    # theme
    "pinax_theme_bootstrap",
    
    # external
    "notification", # must be first
    "staticfiles",
    "compressor",
    "debug_toolbar",
    "django_openid",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
    "idios",
    "metron",
    'south',
    'sorl.thumbnail',
    'social_auth',
    'pybb',
    'pytils',
    'pure_pagination',
    'messages',
    "djcelery",

    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    
    # project
    "about",
    "profiles",
    "tournaments",
]

"""FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]"""

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

PYBB_TEMPLATE = "pybb_base.html"

CONTACT_EMAIL = "support@ahgl.tv"

AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

AUTHENTICATION_BACKENDS = [
    "pinax.apps.account.auth_backends.AuthenticationBackend",
    "social_auth.backends.facebook.FacebookBackend",
]

SOCIAL_AUTH_PIPELINE = (
                        'social_auth.backends.pipeline.social.social_auth_user',
                        'social_auth.backends.pipeline.associate.associate_by_email',
                        'apps.profiles.pipeline.user.get_username',
                        'apps.profiles.pipeline.user.create_user',
                        'social_auth.backends.pipeline.social.associate_user',
                        'social_auth.backends.pipeline.social.load_extra_data',
                        'social_auth.backends.pipeline.user.update_user_details',
                        )

SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook',)

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = True

FACEBOOK_APP_ID              = ''  # REMOVED BECAUSE SECRET
FACEBOOK_API_SECRET          = ''  # REMOVED BECAUSE SECRET
FACEBOOK_EXTENDED_PERMISSIONS = ('email',)

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "what_next"
LOGOUT_REDIRECT_URLNAME = "home"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"

#Cache settings
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Email info
# REMOVED BECAUSE INCLUDES PASSWORDS

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console":{
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler"
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "propagate": True,
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

# Gondor Settings Should Always Be Right BEFORE local_settings Import
GONDOR_LOCAL_SETTINGS = False
GONDOR_REDIS_HOST = None

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

if GONDOR_LOCAL_SETTINGS:
    if GONDOR_REDIS_HOST:
        # Caching
        CACHES = {
            "default": {
                "BACKEND": "redis_cache.RedisCache",
                "LOCATION": ":".join([GONDOR_REDIS_HOST, str(GONDOR_REDIS_PORT)]),
                "OPTIONS": {
                    "DB": 0,
                    "PASSWORD": GONDOR_REDIS_PASSWORD,
                }
            }
        }
        THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
        THUMBNAIL_REDIS_DB = 0
        THUMBNAIL_REDIS_PASSWORD = GONDOR_REDIS_PASSWORD
        THUMBNAIL_REDIS_HOST = GONDOR_REDIS_HOST
        THUMBNAIL_REDIS_PORT = GONDOR_REDIS_PORT
        
    BROKER_TRANSPORT = "redis"
    BROKER_HOST = GONDOR_REDIS_HOST
    BROKER_PORT = GONDOR_REDIS_PORT
    BROKER_VHOST = "0"
    BROKER_PASSWORD = GONDOR_REDIS_PASSWORD
    
    CELERY_RESULT_BACKEND = "redis"
    CELERY_REDIS_HOST = GONDOR_REDIS_HOST
    CELERY_REDIS_PORT = GONDOR_REDIS_PORT
    CELERY_REDIS_PASSWORD = GONDOR_REDIS_PASSWORD