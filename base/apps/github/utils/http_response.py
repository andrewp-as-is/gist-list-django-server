import os

from base.conf import HTTP_CLIENT_DIR


def get_disk_path(relpath):
    return os.path.join(HTTP_CLIENT_DIR, relpath)


# api.github.com/gists/gist/ID


def get_api_gists_disk_path(gist_id):
    relpath = "api.github.com/gists/gist/%s" % gist_id
    return get_disk_path(relpath)


# api.github.com/user/ID user profile


def get_api_user_profile_disk_path(user_id):
    relpath = "api.github.com/user/%s/profile" % user_id
    return get_disk_path(relpath)


# api.github.com/user/ID/gists user gists


def get_api_user_gists_pagination_disk_path(user_id):
    relpath = "api.github.com/user/%s/gists" % user_id
    return get_disk_path(relpath)


def get_api_user_gists_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_user_gists_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# api.github.com/gists authenticated user gists


def get_api_viewer_gists_pagination_disk_path(user_id):
    relpath = "api.github.com/viewer/%s/gists/" % user_id
    return get_disk_path(relpath)


def get_api_viewer_gists_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_viewer_gists_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


def get_api_gists_gist_disk_path(gist_id):
    relpath = "api.github.com/gists/gist/%s" % gist_id
    return get_disk_path(relpath)


# api.github.com/gists/starred authenticated user stars


def get_api_viewer_gists_starred_pagination_disk_path(user_id):
    relpath = "api.github.com/viewer/%s/gists_starred" % user_id
    return get_disk_path(relpath)


def get_api_viewer_gists_starred_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_viewer_gists_starred_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# user/ID/followers


def get_api_user_followers_pagination_disk_path(user_id):
    relpath = "api.github.com/user/%s/followers" % user_id
    return get_disk_path(relpath)


def get_api_user_followers_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_user_followers_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# user/ID/following


def get_api_user_following_pagination_disk_path(user_id):
    relpath = "api.github.com/user/%s/following" % user_id
    return get_disk_path(relpath)


def get_api_user_following_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_user_following_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# api.github.com/graphql user followers


def get_api_graphql_user_followers_pagination_disk_path(user_id):
    relpath = "api.github.com/graphql/user/%s/followers" % user_id
    return get_disk_path(relpath)


def get_api_graphql_user_followers_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_graphql_user_followers_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# api.github.com/graphql user following


def get_api_graphql_user_following_pagination_disk_path(user_id):
    relpath = "api.github.com/graphql/user/%s/following" % user_id
    return get_disk_path(relpath)


def get_api_graphql_user_following_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_graphql_user_following_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# api.github.com/graphql user gists


def get_api_graphql_user_gists_pagination_disk_path(user_id):
    relpath = "api.github.com/graphql/user/%s/gists" % user_id
    return get_disk_path(relpath)


def get_api_graphql_user_gists_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_graphql_user_gists_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))


# api.github.com/graphql gists


def get_api_graphql_viewer_gists_pagination_disk_path(user_id):
    relpath = "api.github.com/graphql/viewer/%s/gists" % user_id
    return get_disk_path(relpath)


def get_api_graphql_viewer_gists_pagination_page_disk_path(user_id, page):
    pagination_disk_path = get_api_graphql_viewer_gists_pagination_disk_path(user_id)
    return os.path.join(pagination_disk_path, str(page))
