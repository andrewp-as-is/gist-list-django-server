import os
import sys

from configurations import Configuration, values
from django_installed_apps_generator import INSTALLED_APPS
import django_exception


def excepthook(exc_type, exc_message, tb):
    django_exception.excepthook(exc_type, exc_message, tb)
    raise exc_type(exc_message)


sys.excepthook = excepthook


# https://github.com/settings/developers
GITHUB_OAUTH_CALLBACK_PATH = "auth/github/callback"

INSTALLED_APPS = (
    list(
        filter(
            lambda s: s.strip() and s.strip()[0] != "#",
            open("settings/INSTALLED_APPS.txt").read().splitlines(),
        )
    )
    + INSTALLED_APPS
)
MIDDLEWARE = list(
    filter(
        lambda s: s.strip() and s.strip()[0] != "#",
        open("settings/MIDDLEWARE.txt").read().splitlines(),
    )
)
context_processors = list(
    filter(
        lambda s: s.strip() and s.strip()[0] != "#",
        open("settings/context_processors.txt").read().splitlines(),
    )
)
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "django_exception": {
            "level": "ERROR",
            "class": "django_exception.ExceptionLogHandler",
        },
    },
    "root": {
        "handlers": ["console", "django_exception"],
        "level": "DEBUG",
    },
    "loggers": {
        "django_exception": {
            "level": "ERROR",
            "handlers": ["django_exception"],
            "propagate": True,
        },
    },
}


class Base(Configuration):
    DATABASES = values.DatabaseURLValue(environ_name="DJANGO_DATABASE_URL")
    INSTALLED_APPS = INSTALLED_APPS
    MIDDLEWARE = MIDDLEWARE
    GITHUB_OAUTH_CLIENT_ID = os.getenv("DJANGO_GITHUB_OAUTH_CLIENT_ID")
    GITHUB_OAUTH_SECRET = os.getenv("DJANGO_GITHUB_OAUTH_SECRET")
    # https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps#scopes
    GITHUB_OAUTH_SCOPES = ["gist", "delete_gist", "star_gist", "private_gist"]
    GITHUB_OAUTH_CALLBACK_URL = "TODO (Dev/Prod)"
    AUTH_USER_MODEL = "user.User"
    ROOT_URLCONF = "urls"
    # STATICFILES_DIRS = [
    #    BASE_DIR / 'dist'  # the directory webpack outputs to
    # ]
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOGIN_REDIRECT_URL = "/"
    LOGIN_URL = "/"
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    # SESSION_ENGINE='base.apps.site_sessions.backends.db'
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(os.getcwd(), "templates")],
            "APP_DIRS": True,
            "OPTIONS": {"context_processors": context_processors},
        },
    ]
    TIME_ZONE = "UTC"
    LANGUAGES = [
        # ('de', _('German')),
        ("en", "English"),
    ]
    LOGGING = LOGGING


class Dev(Base):
    DEBUG = True
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
    MANIFEST_LOADER = {
        "output_dir": "assets/webpack_bundles/dev",
        "manifest_file": "manifest.json",
    }
    STATICFILES_DIRS = [
        "static",
        "assets/webpack_bundles/prod",
    ]
    STATIC_ROOT = "static_cdn"
    STATIC_URL = "/static/"
    GITHUB_OAUTH_CALLBACK_URL = "http://127.0.0.1:8000/%s" % GITHUB_OAUTH_CALLBACK_PATH


class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS = ["*"]
    MANIFEST_LOADER = {"output_dir": "static", "manifest_file": "manifest.json"}
    GITHUB_OAUTH_CALLBACK_URL = "https://domain.com/%s" % GITHUB_OAUTH_CALLBACK_PATH
