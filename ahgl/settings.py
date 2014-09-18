# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os
import os.path
import posixpath
import djcelery

from datetime import timedelta

gettext = lambda s: s

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

djcelery.setup_loader()

INTERNAL_IPS = [
    "127.0.0.1",
    "192.168.0.2",
]

ALLOWED_HOSTS = [".afterhoursgaming.tv", ".ahgl.tv"]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DB_POOL_SIZE = 4
USE_DB_CONNECTION_POOLING = True

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

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

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

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = True
COMPRESS_STORAGE = "staticfiles.storage.StaticFileStorage"
# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

COMPRESS_PARSER = "compressor.parser.Html5LibParser"
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    "johnny.middleware.QueryCacheMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    "account.middleware.TimezoneMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "utils.middleware.RedirectFallbackMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
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
    "cms.context_processors.media",
    "sekizai.context_processors.sekizai",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "staticfiles.context_processors.static",

    "notification.context_processors.notification",
    "django_messages.context_processors.inbox",

    #"pybb.context_processors.processor",

    #"tournaments.context_processors.tournament",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.redirects",
    "django.contrib.sites",
    "django_extensions",

    # theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",

    # external
    "notification",  # must be first
    'account',
    "staticfiles",
    "compressor",
    "debug_toolbar",
    "django_openid",
    "timezones",
    "announcements",
    "pagination",
    "idios",
    "metron",
    'south',
    'sorl.thumbnail',
    'social_auth',

    #'pybb',
    'pytils',
    'pure_pagination',
    'django_messages',
    "djcelery",
    'tinymce',
    'recaptcha_form',
    'raven.contrib.django',
    'clear_cache',
    'phileo',

    # cms
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.teaser',
    'cms.plugins.video',
    'cms.plugins.twitter',

    # project
    "profiles",
    "tournaments",
    "utils",
    'api',

    'rest_framework',
    'corsheaders',
]

REST_FRAMEWORK = {
    'PAGINATE_BY': 10
}

CORS_ORIGIN_WHITELIST = (
    'localhost:9000',
)

CELERYBEAT_SCHEDULE = {
    'expunge-deleted-account': {
        'task': 'profiles.tasks.expunge_deleted',
        'schedule': timedelta(days=1),
    },
}

# FIXTURE_DIRS = [
#     os.path.join(PROJECT_ROOT, "fixtures"),
# ]

PAGINATION_INVALID_PAGE_RAISES_404 = True

TINYMCE_DEFAULT_CONFIG = {
    'theme': "simple",
    'custom_undo_redo_levels': 10,
    'width': "100%",
    'height': "480",
}

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

#Queryset caching with johnny-cache
JOHNNY_TABLE_WHITELIST = [
    'cms_cmsplugin',
    'cms_globalpagepermission',
    'cms_globalpagepermissions_sites',
    'cms_page',
    'cms_page_placeholders',
    'cms_pagemoderator',
    'cms_pagemoderatorstate',
    'cms_pagepermission',
    'cms_pageuser',
    'cms_pageusergroup',
    'cms_placeholder',
    'cms_title',
    'cmsplugin_tournamentpluginmodel',
    'cmsplugin_gamepluginmodel',
    'cmsplugin_file',
    'cmsplugin_googlemap',
    'cmsplugin_link',
    'cmsplugin_picture',
    'cmsplugin_snippetptr',
    'cmsplugin_teaser',
    'cmsplugin_text',
    'cmsplugin_twitterrecententries',
    'cmsplugin_twittersearch',
    'cmsplugin_video',
    'menus_cachekey',
    'snippet_snippet',
    'django_site',
    'auth_group',
    'auth_user_groups',
]

CMS_TEMPLATES = (
    ('splash.html', 'Splash Screen'),
    ('tourney_index.html', 'Tournament Index'),
    ('tourney_index_simple.html', 'Tournament Index Simple'),
    ('simple_custom_nav.html', 'Simple with Custom Nav Plugin'),
    ('simple.html', 'Simple'),
    ('super_simple.html', 'Super Simple'),
    ('narrow.html', 'Narrow'),
    ('article.html', 'Article Template'),
)
CMS_VIEW_PERMISSION = False
CMS_MODERATOR = False
CMS_PERMISSION = False
CMS_REDIRECTS = True

PHILEO_LIKABLE_MODELS = {
    "profiles.Caster": {}  # can override default config settings for each model here
}

#PYBB_TEMPLATE = "pybb_base.html"

ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'blockquote', 'br', 'cite', 'code',
                'dd', 'del', 'div', 'dl', 'dt', 'em', 'h2', 'h3', 'h4', 'h5',
                'i', 'iframe', 'img', 'ins', 'li', 'ol', 'p', 'pre', 'q',
                'small', 'span', 'strong', 'sub', 'sup', 'table', 'td', 'th',
                'tr', 'u', 'ul']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'rel', 'target', 'title', 'data-toggle', 'class'],
    'blockquote': ['cite'],
    'q': ['cite'],
    'img': ['src', 'alt', 'title', 'style'],
    'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'],
    'div': ['class', 'id', 'style'],
    'span': ['class'],
    'p': ['style'],
    'table': ['class'],
    'td': ['colspan'],
    'th': ['colspan'],
    'ul': ['class'],
    'li': ['class'],
}
ALLOWED_STYLES = ['float', 'text-align', 'width', 'height']
ALLOWED_CLASSES = ['accordion-group', 'accordion-heading', 'accordion-toggle',
                   'accordion-body', 'accordion-inner', 'clearfix', 'collapse',
                   'bracket', 'bracket-round', 'bracket-item', 'winner', 'team',
                   'seed', 'score', 'team_name', 'team-link', 'thumbnail',
                   'caption', 'thumbnails', 'pull-right', 'pull-left', 'table',
                   'table-striped', 'table-bordered', 'table-hover',
                   'table-condensed', 'error', 'success', 'warning', 'info',
                   'unstyled', 'span1', 'span2', 'span3', 'span4', 'span5',
                   'span6', 'span7', 'span8', ]

CONTACT_EMAIL = "support@afterhoursgaming.tv"

AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

AUTHENTICATION_BACKENDS = [
    "ahgl.auth_backends.FbLikableBackend",
    "ahgl.auth_backends.HybridLikeableBackend",
]

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'profiles.pipeline.user.get_username',
    'profiles.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook',)

SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = True

FACEBOOK_EXTENDED_PERMISSIONS = ('email',)

LOGIN_URL = "/account/login/"  # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "acct_email"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"

#Cache settings
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CACHEMAGIC_PRECOMPUTE_RELATED_CACHE = False

# Email info
EMAIL_HOST = "oxmail1.registrar-servers.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "support@afterhoursgaming.tv"
SERVER_EMAIL = "support@afterhoursgaming.tv"
DEFAULT_FROM_EMAIL = "support@afterhoursgaming.tv"
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": '[%(levelname)s] %(name)s: %(message)s'
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "null": {
            "level": "DEBUG",
            "class": "django.utils.log.NullHandler"
        }
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["null"],
            "propagate": False,
            "level": "DEBUG"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *  # noqa
except ImportError:
    pass
