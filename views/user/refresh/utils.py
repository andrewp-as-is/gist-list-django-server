import time

import requests

from base.apps.github.models import User
from base.apps.github.utils import get_api_timestamp

def get_github_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass


def create_github_user(data):
    defaults = {
        "login": data["login"],
        "name": data["name"],
        "blog": data["blog"],
        "location": data["location"],
        "twitter_username": data["twitter_username"],
        "public_gists_count": data["public_gists"],
        "followers_count": data["followers"],
        "following_count": data["following"],
        "created_at": get_api_timestamp(data["created_at"]),
        "updated_at": get_api_timestamp(data["updated_at"]),
    }
    user, created = User.objects.get_or_create(defaults, id=data["id"])
    return user


def get_github_user_data(login, token):
    attempts_count = 0
    url = "https://api.github.com/users/%s" % login
    headers = {"Authorization": "Bearer %s" % access_token}
    attempts_count = 0
    while True:
        attempts_count += 1
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            if attempts_count > 3:
                r.raise_for_status()


"""
def get_user_id(login):
    # https://github.com/LOGIN.png -> https://avatars.githubusercontent.com/u/ID?v=4
    url = 'https://github.com/%s.png' % login
    r = requests.head(url,allow_redirects=False)
    redirect = headers.get('location',None)
    if 'avatars.githubusercontent.com' in redirect:
        return redirect.split('/')[-1].split('?')[-1]
"""
