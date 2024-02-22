import time

from django.conf import settings
import requests

from base.apps.github.models import Token, User as GithubUser, User, UserMapping
from base.apps.github.utils import get_api_timestamp
from base.apps.user.models import User

"""
https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
"""

def create_user(data):
    defaults = {'login':data['login']}
    user, created = User.objects.update_or_create(defaults,id=data['id'])
    return user

def create_github_user(data):
    followers_change, following_change = True, True
    try:
        github_user = GithubUser.objects.get(id=data['id'])
        change_data = {}
        if data['followers']!=github_user.followers_count:
            followers_change = True
        if data['following']!=github_user.following_count:
            following_change = True
        new_user = False
    except GithubUser.DoesNotExist:
        followers_change=data['followers']>0
        following_change=data['following']>0
        new_user = True
    defaults = {
        'login':data['login'],
        'name':data['name'],
        'blog':data['blog'],
        'location':data['location'],
        'twitter_username':data['twitter_username'],
        'public_gists_count':data['public_gists'],
        'followers_count':data['followers'],
        'following_count':data['following'],
        'created_at':get_api_timestamp(data['created_at']),
        'updated_at':get_api_timestamp(data['updated_at'])
    }
    GithubUser.objects.update_or_create(defaults,id=data['id'])
    defaults =dict(created_at=int(time.time()))
    UserMapping.objects.get_or_create(defaults,login=data['login'],user_id=data['id'])

def create_github_token(user_id,token):
    defaults = {
        'token':token,
        'core_ratelimit_limit':5000,
        'core_ratelimit_remaining':5000,
        'core_ratelimit_reset':None,
        'graphql_ratelimit_limit':5000,
        'graphql_ratelimit_remaining':5000,
        'graphql_ratelimit_reset':None,
        'created_at':int(time.time())
    }
    token,created = Token.objects.get_or_create(defaults,user_id=user_id)

def create_user(data):
    try:
        user = User.objects.get(login=data['login'])
        if data['login']!=user.login:
            User.objects.filter(id=data['id']).update(login=data['login'])
    except User.DoesNotExist:
        user, created = User(id=data['id'],login=data['login']).save()
    return user

def get_access_token(code):
    data = {
        'code': code,
        'client_id': settings.GITHUB_OAUTH_CLIENT_ID,
        'client_secret': settings.GITHUB_OAUTH_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.GITHUB_OAUTH_CALLBACK_URL
    }
    url = 'https://github.com/login/oauth/access_token'
    attempts_count=0
    while True:
        attempts_count+=1
        r = requests.post(url,data=data,timeout=10)
        if r.status_code==200:
            # access_token=XXX&scope=gist&token_type=bearer
            for s in filter(lambda s: 'access_token' in s, r.text.split('&')):
                return s.split('=')[1]
            raise ValueError(r.text)
        else:
            if attempts_count>3:
                r.raise_for_status()
