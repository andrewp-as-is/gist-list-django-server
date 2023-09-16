import json
from datetime import date, datetime, timedelta
import time

from django.apps import apps
from django.db import transaction
from django.utils.timesince import timesince as _timesince
import requests

from base.apps.github_matview.models import Gist as MatviewGist
from base.apps.github_matview_new.models import Gist as NewMatviewGist
from base.apps.github.models import UserRefreshLock, UserRefreshViewer
from base.apps.github.utils.graphql import get_user_followers_query, get_user_following_query, get_viewer_gists_query, get_user_gists_query
from base.apps.github.utils.http_response import get_api_viewer_gists_pagination_page_relpath, get_api_viewer_gists_starred_pagination_page_relpath, get_api_graphql_user_followers_pagination_page_relpath, get_api_graphql_user_following_pagination_page_relpath, get_api_graphql_viewer_gists_pagination_page_relpath, get_api_graphql_user_gists_pagination_page_relpath
from base.apps.http_request.models import Job as RequestJob
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
    authenticated = user.id==token.user_id
    if authenticated: # authenticated user (unknown pages count)
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
    else: # public user
        url = 'https://api.github.com/user/%s' % user.id
        url2relpath[url] = 'api.github.com/user/%s/profile' % user.id
        # todo: etag. no need all requests if no changes. where to check?
        if user.public_gists_count:
            # &page=1 request only
            url = 'https://api.github.com/user/%s/gists?per_page=100&page=%s' % (user.id,1)
            url2relpath[url] = 'api.github.com/user/%s/gists/%s' % (user.id,1)
            # graphql user gists - `files` `language` not supported
            url = 'https://api.github.com/graphql?schema=user.gists&user_id=%s' % user.id
            url2relpath[url] = get_api_graphql_user_gists_pagination_page_relpath(user.id,1)
            url2query[url] = get_user_gists_query(user.login)
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
        create_list+=[UserRefreshLock(
            user_id=user.id,
            authenticated=authenticated,
            timestamp=int(time.time())
        )]
        create_list+=[UserRefreshViewer(
            user_id=user.id,
            viewer_id=token.user_id,
            timestamp=int(time.time())
        )]
    with transaction.atomic():
        bulk_create(create_list)

def timesince(d):
    yesterday = date.today() - timedelta(days = 1)
    td = datetime.now() - d
    td_seconds = td.total_seconds()
    td_hours = int(td_seconds / (60*60))
    if td.days == 0 and td.total_seconds()<60:
        return 'now'
    if td.days == 0 and not td_hours:
        return '%s ago' % _timesince(d).split(',')[0]
    if td.days == 0 and td.total_seconds()<60*60*2:
        return '1 hour ago'
    if td.days == 0  or (d.date() == yesterday and td_hours<=23):
        return '%s hours ago' % td_hours
    if d.date() == yesterday:
        return 'yesterday'
    if td.days<=31:
        return '%s days ago' % td.days
    return '%s ago' % _timesince(d).split(',')[0]
