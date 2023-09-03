import os

from base.settings.configurations import Base
from base.settings.utils import get_context_processors

# https://github.com/settings/developers
GITHUB_OAUTH_CALLBACK_PATH = 'auth/github/callback'


class Base(Base):
    GITHUB_OAUTH_CLIENT_ID = os.getenv('DJANGO_GITHUB_OAUTH_CLIENT_ID')
    GITHUB_OAUTH_SECRET = os.getenv('DJANGO_GITHUB_OAUTH_SECRET')
    # https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps#scopes
    GITHUB_OAUTH_SCOPES = ['gist','delete_gist','star_gist','private_gist']
    GITHUB_OAUTH_CALLBACK_URL = 'TODO (Dev/Prod)'
    AUTH_USER_MODEL = 'user.User'
    ROOT_URLCONF='urls'
    #STATICFILES_DIRS = [
    #    BASE_DIR / 'dist'  # the directory webpack outputs to
    #]
    DATETIME_FORMAT='%Y-%m-%d %H:%M:%S'
    LOGIN_REDIRECT_URL='/'
    LOGIN_URL='/'
    SECRET_KEY=os.getenv('DJANGO_SECRET_KEY')
    # SESSION_ENGINE='base.apps.site_sessions.backends.db'
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(),'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': get_context_processors()
            },
        },
    ]
    TIME_ZONE='UTC'
    LANGUAGES = [
        # ('de', _('German')),
        ('en', 'English'),
    ]


class Dev(Base):
    DEBUG = True
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    MANIFEST_LOADER = {
        'output_dir': 'assets/webpack_bundles/dev',
        'manifest_file': 'manifest.json'
    }
    STATICFILES_DIRS=[
        'static',
        'assets/webpack_bundles/prod',
    ]
    STATIC_ROOT='static_cdn'
    STATIC_URL='/static/'
    GITHUB_OAUTH_CALLBACK_URL = 'http://127.0.0.1:8000/%s' % GITHUB_OAUTH_CALLBACK_PATH

class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    MANIFEST_LOADER = {
        'output_dir': 'static',
        'manifest_file': 'manifest.json'
    }
    GITHUB_OAUTH_CALLBACK_URL = 'https://domain.com/%s' % GITHUB_OAUTH_CALLBACK_PATH
