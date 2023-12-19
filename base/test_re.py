import os
import re
from urllib.parse import parse_qs, urlparse

from linkheader_parser import parse


PATTERN2TEMPLATE = {
    'gists/gist/[\w]+':"gists/gist/{gist_id}",
    #'user/[\d]+/profile':get_rest_api_user_profile_disk_relpath,
    #'user/[\d]+/gists/[\w]+':get_rest_api_user_gists_disk_relpath,
    #'gists?+':get_rest_api_viewer_gists_disk_relpath,
    #'gists/starred?+':get_rest_api_viewer_gists_starred_disk_relpath,
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
    return {}

def get_disk_path(url):
    for regex,template in REGEX2TEMPLATE.items():
        if regex.match(url.replace('https://api.github.com/','')):
            disk_relpath = template.format(**get_params(url))
            return os.path.join('HTTP_CLIENT_DIR','api.github.com',disk_relpath)

def get_rest_api_gists_disk_relpath(gist_id):
    return "gists/gist/{gist_id}" % gist_id

def get_rest_api_user_profile_disk_relpath(user_id):
    return "user/%s/profile" % user_id

def get_rest_api_user_gists_disk_relpath(user_id, page):
    return "user/%s/gists/%s" % (user_id,page)

def get_rest_api_viewer_gists_disk_relpath(user_id, page):
    return "viewer/%s/gists/%s" % (user_id, page)

def get_rest_api_viewer_gists_starred_disk_relpath(user_id, page):
    return "viewer/%s/gists_starred" % (user_id, page)

def get_rest_api_user_followers_disk_relpath(user_id, page):
    return "user/%s/followers/%s" % (user_id, page)

def get_rest_api_user_following_disk_relpath(user_id, page):
    return "user/%s/following/%s" % (user_id, page)

# api.github.com/graphql user followers


def get_graphql_api_graphql_user_followers_disk_relpath(user_id, page):
    return "graphql/user/%s/followers/%s" % (user_id, page)

def get_graphql_api_graphql_user_following_disk_relpath(user_id, page):
    return "graphql/user/%s/following/%s" % (user_id, page)

def get_graphql_api_graphql_user_gists_disk_relpath(user_id, page):
    return "graphql/user/%s/gists/%s" % (user_id, page)

def get_graphql_api_graphql_viewer_gists_disk_relpath(user_id, page):
    return "graphql/user/%s/viewer/%s" % (user_id, page)

regex = re.compile('https://api.github.com/gists/gist/[\w]+')
url = 'https://api.github.com/gists/gist/AAAb000test42'
print(regex.match(url))
