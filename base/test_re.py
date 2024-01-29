import os
import re
from urllib.parse import parse_qs, urlparse

from linkheader_parser import parse


PATTERN2TEMPLATE = {
    # gist.githubusercontent.com
    '[\w]+/[\w]+/raw/[\w]+':"raw/{user_id}/{gist_id}/{filename}",
    # api.github.com
    'gists/gist/[\w]+':"gists/gist/{gist_id}",
    'user/[\d]+$':"user/{user_id}/profile",
    'user/[\d]+/gists?+':"user/{user_id}/gists/{page}",
    'user/[\d]+/followers?+':"user/{user_id}/followers/{page}",
    'user/[\d]+/following?+':"user/{user_id}/following/{page}",
    'gists?+':"viewer/{user_id}/gists/{page}",
    'gists/starred?+':"viewer/{user_id}/gists_starred/{page}",
    'graphql\?schema=user\.followers':'graphql/user/{user_id}/followers/{page}',
    'graphql\?schema=user\.following':'graphql/user/{user_id}/following/{page}',
    'graphql\?schema=user\.gists':'graphql/user/{user_id}/gists/{page}',
    'graphql\?schema=viewer\.gists':'graphql/viewer/{user_id}/gists/{page}',
}
REGEX2TEMPLATE = {re.compile(p):f for p,f in PATTERN2TEMPLATE.items()}


def get_filename(url):
    return url.split('/')[-1].split('?')[0]

def get_gist_id(url):
    if 'gist.githubusercontent.com' in url:
        return url.split('gist.githubusercontent.com/')[1].split('/')[1]
    if '/gists/gist/' in url:
        return url.split('/gists/gist/')[1].split('/')[-1]

def get_page(url):
    if '&page=' in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["page"][0])


def get_user_id(url):
    if "user_id" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["user_id"][0])
    if "https://api.github.com/user/" in url:
        return int(url.replace("https://api.github.com/user/", "").split("/")[0])

def get_params(url):
    return {
        'user_id':get_user_id(url),
        'gist_id':get_gist_id(url),
        'page':get_page(url),
        'filename':get_filename(url)
    }

def get_disk_path(url):
    host = url.split("//")[-1].split("/")[0].split('?')[0]
    for regex,template in REGEX2TEMPLATE.items():
        if regex.match(url.replace('https://%s/' % host,'')):
            disk_relpath = template.format(**get_params(url))
            return os.path.join('HTTP_CLIENT_DIR','api.github.com',disk_relpath)


url = 'https://api.github.com/graphql?schema=user.followers&user_id=13243941&login=andrewp-as-is&page=1'
url = 'https://gist.githubusercontent.com/user/GIST_ID/raw/FILENAME?user_id=42'
print(get_disk_path(url))
# todo: user_id
