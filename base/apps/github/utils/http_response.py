import os

# api.github.com/gists/gist/ID

def get_api_gists_gist_relpath(gist_id):
    return 'api.github.com/gists/gist/%s' % gist_id

# api.github.com/user/ID user profile

def get_api_user_profile_relpath(user_id):
    return 'api.github.com/user/%s/profile' % user_id

# api.github.com/user/ID/gists user gists

def get_api_user_gists_pagination_relpath(user_id):
    return 'api.github.com/user/%s/gists' % user_id

def get_api_user_gists_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_user_gists_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))


# api.github.com/gists authenticated user gists

def get_api_viewer_gists_pagination_relpath(user_id):
    return 'api.github.com/viewer/gists/%s' % user_id

def get_api_viewer_gists_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_viewer_gists_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

def get_api_gists_gist_relpath(gist_id):
    return 'api.github.com/gists/gist/%s' % gist_id

# api.github.com/gists/starred authenticated user stars

def get_api_viewer_gists_starred_pagination_relpath(user_id):
    return 'api.github.com/viewer/%s/gists/starred' % user_id

def get_api_viewer_gists_starred_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_viewer_gists_starred_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

# user/ID/followers

def get_api_user_followers_pagination_relpath(user_id):
    return 'api.github.com/user/%s/followers' % user_id

def get_api_user_followers_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_user_followers_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

# user/ID/following

def get_api_user_following_pagination_relpath(user_id):
    return 'api.github.com/user/%s/following' % user_id

def get_api_user_following_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_user_following_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

# api.github.com/graphql user followers

def get_api_graphql_user_followers_pagination_relpath(user_id):
    return 'api.github.com/graphql/user/%s/followers' % user_id

def get_api_graphql_user_followers_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_graphql_user_followers_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

# api.github.com/graphql user following

def get_api_graphql_user_following_pagination_relpath(user_id):
    return 'api.github.com/graphql/user/%s/followers' % user_id

def get_api_graphql_user_following_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_graphql_user_following_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

# api.github.com/graphql user gists

def get_api_graphql_user_gists_pagination_relpath(user_id):
    return 'api.github.com/graphql/user/%s/gists' % user_id

def get_api_graphql_user_gists_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_graphql_user_gists_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))

# api.github.com/graphql gists

def get_api_graphql_viewer_gists_pagination_relpath(user_id):
    return 'api.github.com/graphql/viewer/%s/gists' % user_id

def get_api_graphql_viewer_gists_pagination_page_relpath(user_id,page):
    pagination_relpath = get_api_graphql_viewer_gists_pagination_relpath(user_id)
    return os.path.join(pagination_relpath,str(page))
