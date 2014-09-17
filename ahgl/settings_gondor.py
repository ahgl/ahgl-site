import os
import urlparse

from .settings import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = DEBUG

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "WARNING",
        "handlers": ["sentry"],
    },
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "sentry": {
            "level": "ERROR",
            "class": "raven.contrib.django.handlers.SentryHandler",
        },
        "console": {
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
        "raven": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    }
}

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])
    GONDOR_REDIS_HOST = url.hostname
    GONDOR_REDIS_PORT = url.port
    GONDOR_REDIS_PASSWORD = url.password

    # Caching
    CACHES = {
        "default": {
            "BACKEND": "cachemagic.cache.RedisHerdCache",
            "LOCATION": ":".join([GONDOR_REDIS_HOST, str(GONDOR_REDIS_PORT)]),
            "OPTIONS": {
                "DB": 0,
                "PASSWORD": GONDOR_REDIS_PASSWORD,
            },
        },
        "johnny": {
            "BACKEND": "johnny.backends.redis.RedisCache",
            "LOCATION": ":".join([GONDOR_REDIS_HOST, str(GONDOR_REDIS_PORT)]),
            "OPTIONS": {
                "DB": 0,
                "PASSWORD": GONDOR_REDIS_PASSWORD,
            },
            "JOHNNY_CACHE": True,
        },
    }

    BROKER_TRANSPORT = "redis"
    BROKER_HOST = GONDOR_REDIS_HOST
    BROKER_PORT = GONDOR_REDIS_PORT
    BROKER_VHOST = "0"
    BROKER_PASSWORD = GONDOR_REDIS_PASSWORD

    import djcelery
    djcelery.setup_loader()
    CELERY_RESULT_BACKEND = "redis"
    CELERY_REDIS_HOST = GONDOR_REDIS_HOST
    CELERY_REDIS_PORT = GONDOR_REDIS_PORT
    CELERY_REDIS_PASSWORD = GONDOR_REDIS_PASSWORD

if "GONDOR_HAYSTACK_SOLR_URL" in os.environ:
    if 'HAYSTACK_SEARCH_ENGINE' in locals():
        del HAYSTACK_SEARCH_ENGINE  # noqa
    GONDOR_HAYSTACK_SOLR_URL = os.environ["GONDOR_HAYSTACK_SOLR_URL"]
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': GONDOR_HAYSTACK_SOLR_URL
            # ...or for multicore...
            # 'URL': 'http://127.0.0.1:8983/solr/mysite',
        },
    }

SITE_ID = 1  # set this to match your Sites setup

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "media")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "static")

MEDIA_URL = "/site_media/media/"  # make sure this maps inside of a static_urls URL
STATIC_URL = "/site_media/static/"  # make sure this maps inside of a static_urls URL
MEDIA_URL = os.environ.get('MEDIA_URL', MEDIA_URL)
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"
ADMIN_MEDIA_PREFIX = os.environ.get('ADMIN_MEDIA_PREFIX', ADMIN_MEDIA_PREFIX)

CMS_MEDIA_PATH = "cms/"
CMS_MEDIA_ROOT = os.path.join(MEDIA_ROOT, CMS_MEDIA_PATH)
CMS_MEDIA_URL = posixpath.join(MEDIA_URL, CMS_MEDIA_PATH)
CMS_PAGE_MEDIA_PATH = "cms_page_media/"
CMS_VIEW_PERMISSION = False

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "AHGLtv"
SERVER_EMAIL = "support@afterhoursgaming.tv"
DEFAULT_FROM_EMAIL = "support@afterhoursgaming.tv"
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

FILE_UPLOAD_PERMISSIONS = 0640

# Gondor stores secret settings in environ variables, load them up here
SECRET_KEY = os.environ['SECRET_KEY']
FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
FACEBOOK_API_SECRET = os.environ['FACEBOOK_API_SECRET']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
RECAPTCHA_PUB_KEY = os.environ['RECAPTCHA_PUB_KEY']
RECAPTCHA_PRIV_KEY = os.environ['RECAPTCHA_PRIV_KEY']
SENTRY_DSN = os.environ['SENTRY_DSN']
if os.environ.get('INTERNAL_IPS'):
    INTERNAL_IPS = INTERNAL_IPS + tuple(os.environ['INTERNAL_IPS'].split(":"))
DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', 4))
USE_DB_CONNECTION_POOLING = os.environ.get('USE_DB_CONNECTION_POOLING', "True") == "True"
