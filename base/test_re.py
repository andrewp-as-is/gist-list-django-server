import os
import re
from urllib.parse import parse_qs, urlparse

from linkheader_parser import parse


PATTERN2TEMPLATE = {
    'gists/gist/[\w]+':"gists/gist/{gist_id}",
    'user/[\d]+$':"user/{user_id}/profile",
    'user/[\d]+/gists?+':"user/{user_id}/gists/{page}",
    'user/[\d]+/followers?+':"user/{user_id}/followers/{page}",
    'user/[\d]+/following?+':"user/{user_id}/following/{page}",
    'gists?+':"viewer/{user_id}/gists/{page}",
    'gists/starred?+':"viewer/{user_id}/gists_starred/{page}",
    'graphql\?schema=user\.followers':'graphql/user/%s/followers/{page}',
    'graphql\?schema=user\.following':'graphql/user/%s/following/{page}',
    'graphql\?schema=user\.gists':'graphql/user/%s/gists/{page}',
    'graphql\?schema=viewer\.gists':'graphql/viewer/%s/gists/{page}',
}
REGEX2TEMPLATE = {re.compile(p):f for p,f in PATTERN2TEMPLATE.items()}

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
    return {}

def get_disk_path(url):
    print(url.replace('https://api.github.com/',''))
    for regex,template in REGEX2TEMPLATE.items():
        if regex.match(url.replace('https://api.github.com/','')):
            disk_relpath = template.format(**get_params(url))
            return os.path.join('HTTP_CLIENT_DIR','api.github.com',disk_relpath)


url = 'https://api.github.com/graphql?schema=user.followers&user_id=13243941&page=1'
url = 'https://api.github.com/graphql?schema=user.followers'
print(get_disk_path(url))
