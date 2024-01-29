import os
import re
from urllib.parse import parse_qs, urlparse

from base.apps.http_client.utils import get_disk_path as _get_disk_path

"""
https://gist.githubusercontent.com/USER/GIST/raw/HASH/FILENAME
"""


PATTERN2TEMPLATE = {
    # https://gist.githubusercontent.com/USER/GIST/raw/FILENAME
    '[\w]+/[\w]+/raw/[\w]+':"{user_id}/{gist_id}/{filename}",
    # api.github.com
    'gists/[\w]+':"gists/{gist_id}",
    'user/[\d]+$':"user/{user_id}/profile",
    'user/[\d]+\?+':"user/{user_id}/profile",
    'user/[\d]+/gists\?+':"user/{user_id}/gists/{page}",
    'user/[\d]+/raw/[\d]+/.*':"raw/user/{user_id}/{gist_id}/{filename}",
    'user/[\d]+/followers\?+':"user/{user_id}/followers/{page}",
    'user/[\d]+/following\?+':"user/{user_id}/following/{page}",
    'gists\?+':"viewer/{user_id}/gists/{page}",
    'gists/starred\?+':"viewer/{user_id}/gists_starred/{page}",
    'graphql\?schema=user.followers+':'graphql/user/{user_id}/followers/{page}',
    'graphql\?schema=user.following+':'graphql/user/{user_id}/following/{page}',
    'graphql\?schema=user.gists+':'graphql/user/{user_id}/gists/{page}',
    'graphql\?schema=viewer.gists+':'graphql/viewer/{user_id}/gists/{page}',
}
REGEX2TEMPLATE = {re.compile(p):f for p,f in PATTERN2TEMPLATE.items()}

def get_filename(url):
    return url.split('/')[-1].split('?')[0]

def get_page(url):
    if '&page=' in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["page"][0])

def get_gist_id(url):
    if 'gist.githubusercontent.com' in url:
        return url.split('gist.githubusercontent.com/')[1].split('/')[1]
    if '/gists/gist/' in url:
        return url.split('/gists/gist/')[1].split('/')[-1]

def get_user_id(url):
    if "user_id" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["user_id"][0])
    if "https://api.github.com/user/" in url:
        return int(url.replace("https://api.github.com/user/", "").split("/")[0])

def get_params(url):
    return {
        'user_id':get_user_id(url),
        'gist_id':url.split('/')[-1],
        'page':get_page(url)
    }

def get_disk_path(url):
    host = url.split("//")[-1].split("/")[0].split('?')[0]
    for regex,template in REGEX2TEMPLATE.items():
        if regex.match(url.replace('https://%s/' % host,'')):
            disk_relpath = template.format(**get_params(url))
            return _get_disk_path(os.path.join(host,disk_relpath))
    raise ValueError(url)

