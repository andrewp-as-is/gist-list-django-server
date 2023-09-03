from urllib.parse import urlencode, quote_plus

from django.conf import settings

"""
https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
https://github.com/settings/developers
"""

DATA = {
    'client_id':settings.GITHUB_OAUTH_CLIENT_ID,
    'redirect_uri':settings.GITHUB_OAUTH_CALLBACK_URL,
    'scope': ' '.join(set(settings.GITHUB_OAUTH_SCOPES)),
    'response_type': 'code'
}

def get_url():
    qs = urlencode(DATA, quote_via=quote_plus)
    return 'https://github.com/login/oauth/authorize?'+qs
