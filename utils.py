import json
import time

from django.apps import apps
from django.db import transaction
import requests

from base.apps.github_gist_matview.models import Gist as MatviewGist
from base.apps.github_gist_new_matview.models import Gist as NewMatviewGist
from base.apps.github_user_refresh.models import Lock
from base.apps.github.utils.graphql import get_user_followers_query, get_user_following_query, get_viewer_gists_query
from base.apps.github.utils.http_response import get_api_viewer_gists_pagination_page_relpath, get_api_viewer_gists_starred_pagination_page_relpath, get_api_graphql_user_followers_pagination_page_relpath, get_api_graphql_user_following_pagination_page_relpath, get_api_graphql_viewer_gists_pagination_page_relpath
from base.apps.http_request_job.models import Job as RequestJob
from base.utils import bulk_create

def get_gist_model(user_id):
    if not user_id:
        return MatviewGist
    if NewMatviewGist.objects.filter(owner_id=user_id).only('id').first():
        return NewMatviewGist
    return MatviewGist

def iter_app_model_list(app_label):
    for model in apps.get_models():
        if model._meta.app_label==app_label:
            yield model

def get_gist_language_model(app_label):
    for model in iter_app_model_list(app_label):
        if 'language' in model.__name__.lower():
            return model

def get_gist_tag_model(app_label):
    for model in iter_app_model_list(app_label):
        if 'tag' in model.__name__.lower():
            return model

def get_github_api_data(url,token):
    headers = {"Authorization": "Bearer %s" % token}
    attempts_count=0
    while True:
        attempts_count+=1
        r = requests.get(url,headers=headers,timeout=10)
        if r.status_code==200:
            return r.json()
        if r.status_code==404:
            return
        if attempts_count>3 and r.status_code not in [200,404,429]:
            r.raise_for_status()


def refresh_user(user,token,priority,**options):
    # todo: priority based on user.id vs token.user_id
    # root = 'api.github.com/user/%s' % (user.id)
    url2relpath = {}
    url2query = {}
    """
    if user.followers_count:
        for page in range(1,int(user.followers_count/100)+2):
            url = 'https://api.github.com/user/%s/followers?per_page=100&page=%s' % (user.id,page)
            url2relpath[url] = 'followers/%s' % page
    if user.following_count:
        for page in range(1,int(user.following_count/100)+1):
            url = 'https://api.github.com/user/%s/following?per_page=100&page=%s' % (user.id,page)
            url2relpath[url] = 'following/%s' % page
    """
    url = 'https://api.github.com/graphql?schema=user.followers&user_id=%s' % user.id
    url2relpath[url] = get_api_graphql_user_followers_pagination_page_relpath(user.id,1)
    url2query[url] = get_user_followers_query(user.login)
    url = 'https://api.github.com/graphql?schema=user.following&user_id=%s' % user.id
    url2relpath[url] = get_api_graphql_user_following_pagination_page_relpath(user.id,1)
    url2query[url] = get_user_following_query(user.login)
    if user.id==token.user_id: # authenticated user (unknown pages count)
        # gists/starred api v3 only, graphql not supported
        url = 'https://api.github.com/gists/starred?user_id=%s&per_page=100&page=1' % user.id
        url2relpath[url] = get_api_viewer_gists_starred_pagination_page_relpath(user.id,1)
        # authenticated user gists
        # api v3 authenticated user gists (`files` with `language` )
        url = 'https://api.github.com/gists?user_id=%s&per_page=100&page=1' % (user.id)
        url2relpath[url] = get_api_viewer_gists_pagination_page_relpath(user.id,1)
        # graphql viewer gists - `files` `language` not supported
        url = 'https://api.github.com/graphql?schema=viewer.gists&user_id=%s' % user.id
        url2relpath[url] = get_api_graphql_viewer_gists_pagination_page_relpath(user.id,1)
        url2query[url] = get_viewer_gists_query()
    else:
        url = 'https://api.github.com/user/%s' % user.id
        url2relpath[url] = 'api.github.com/user/%s/info' % user.id
        if user.public_gists_count:
            pass
           # for page in range(1,int(user.public_gists_count/100)+2):
           #     url = 'https://api.github.com/user/%s/gists?per_page=100&page=%s' % (user.id,page)
           #     url2relpath[url] = 'api.github.com/user/%s/gists/%s' % (user.id,page)
    create_list = []
    for url,response_relpath in url2relpath.items():
        headers = "\n".join([
            "Authorization: Bearer %s" % token.token,
            "X-GitHub-Api-Version: 2022-11-28"
        ])
        data = None
        if 'github.com/graphql' in url:
            query = url2query[url]
            data = json.dumps({"query": query.replace('\n','')})
            headers=headers+'\nContent-Type: application/json'
        create_list+=[RequestJob(
            domain = 'api.github.com',
            url = url,
            method='GET' if 'github.com/graphql' not in url else 'POST',
            headers=headers,
            data = data,
            response_relpath=response_relpath,
            priority=priority if '/follow' not in url else 10
        )]
    with transaction.atomic():
        defaults = dict(token_id=token.id,timestamp=int(time.time()))
        lock, created = Lock.objects.get_or_create(defaults,user_id=user.id)
        RequestJob.objects.bulk_create(create_list,ignore_conflicts=True)
