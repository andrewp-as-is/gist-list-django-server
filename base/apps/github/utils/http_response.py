import os
import re
from urllib.parse import parse_qs, urlparse

from linkheader_parser import parse

from base.conf import HTTP_CLIENT_DIR


PATTERN2TEMPLATE = {
    'gists/gist/[\w]+':"gists/gist/{gist_id}",
    'user/[\d]+/profile':"user/{user_id}/profile",
    'user/[\d]+/gists?+':"user/{user_id}/gists/{page}",
    'user/[\d]+/followers?+':"user/{user_id}/followers/{page}",
    'user/[\d]+/following?+':"user/{user_id}/following/{page}",
    'gists?+':"viewer/{user_id}/gists/{page}",
    'gists/starred?+':"viewer/{user_id}/gists_starred/{page}",
}
REGEX2TEMPLATE = {re.compile(p):f for p,f in PATTERN2TEMPLATE.items()}

def get_page(url):
    parsed_url = urlparse(url)
    return int(parse_qs(parsed_url.query)["page"][0])


def get_user_id(url):
    if "user_id" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["user_id"][0])
    if "https://api.github.com/user/" in url:
        return int(url.replace("https://api.github.com/user/", "").split("/")[0])

def get_params(url):
    return {'user_id':get_user_id(url),'page':get_page(url)}

def get_disk_path(url):
    for regex,template in REGEX2TEMPLATE.items():
        if regex.match(url.replace('https://api.github.com/','')):
            disk_relpath = template.format(**get_params(url))
            return os.path.join('HTTP_CLIENT_DIR','api.github.com',disk_relpath)


def get_graphql_api_graphql_user_followers_disk_relpath(user_id, page):
    return "graphql/user/%s/followers/%s" % (user_id, page)

def get_graphql_api_graphql_user_following_disk_relpath(user_id, page):
    return "graphql/user/%s/following/%s" % (user_id, page)

def get_graphql_api_graphql_user_gists_disk_relpath(user_id, page):
    return "graphql/user/%s/gists/%s" % (user_id, page)

def get_graphql_api_graphql_viewer_gists_disk_relpath(user_id, page):
    return "graphql/user/%s/viewer/%s" % (user_id, page)
