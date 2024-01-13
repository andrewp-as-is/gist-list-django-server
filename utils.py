import json
from datetime import date, datetime, timedelta
import os
import time

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils.timesince import timesince as _timesince
import requests

from django_command_worker.models import Queue
from base.apps.github_matview.models import Gist as MatviewGist
from base.apps.github_live_matview.models import Gist as NewMatviewGist
# from base.apps.user.models import GithubGistRefresh,
from base.apps.user.models import GithubUserRefresh, GithubUserRefreshLock
from base.apps.github.utils.graphql import (
    get_user_followers_query,
    get_user_following_query,
    get_viewer_gists_query,
    get_user_gists_query,
)

from base.apps.github.utils.http_response import get_disk_path
from base.apps.http_client.models import RequestJob
from django_bulk_create import bulk_create

def get_github_api_data(url, token):
    headers = {"Authorization": "Bearer %s" % token}
    attempts_count = 0
    while True:
        attempts_count += 1
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 404:
            return
        if attempts_count > 3 and r.status_code not in [200, 404, 429]:
            r.raise_for_status()


def refresh_gist(gist, token, priority, **options):
    url_list = []
    url2query = {}
    headers = {
        "Authorization": "Bearer %s" % token.token,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = "https://api.github.com/gists/%s" % gist.id
    url2relpath[url] = get_api_gists_gist_disk_path(gist.id)
    create_list = []
    for url in url_list:
        data = None
        if "github.com/graphql" in url:
            query = url2query[url]
            data = json.dumps({"query": query.replace("\n", "")})
            headers["Content-Type"] = "application/json"
        create_list += [
            RequestJob(
                host="api.github.com",
                url=url,
                method="GET" if "github.com/graphql" not in url else "POST",
                headers=json.dumps(headers),
                data=data,
                disk_path=get_disk_path(url),
                priority=priority,
            )
        ]
        create_list += [GistRefresh(gist_id=gist.id, timestamp=int(time.time()))]
    with transaction.atomic():
        bulk_create(create_list)


def refresh_user(request,github_user, priority):
    # todo: priority based on user.id vs token.user_id
    # root = 'api.github.com/user/%s' % (user.id)
    url_list = []
    url2query = {}
    token = request.user.token
    headers = {
        "Authorization": "Bearer %s" % token.token,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    # todo: followers/following request
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
    url = "https://api.github.com/user/%s" % github_user.id
    url_list+=[url]
    # graphql user followers
    url = (
        "https://api.github.com/graphql?schema=user.followers&user_id=%s&login=%s&page=1"
        % (github_user.id,github_user.login)
    )
    url_list+=[url]
    url2query[url] = get_user_followers_query(github_user.login)
    # graphql user following
    url = (
        "https://api.github.com/graphql?schema=user.following&user_id=%s&login=%s&page=1"
        % (github_user.id,github_user.login)
    )
    url_list+=[url]
    url2query[url] = get_user_following_query(github_user.login)
    secret = github_user.id == token.user_id
    if secret:  # authenticated user (unknown pages count)
        # gists/starred api v3 only, graphql not supported
        url = (
            "https://api.github.com/gists/starred?user_id=%s&login=%s&per_page=100&page=1"
            % (github_user.id,github_user.login)
        )
        url_list+=[url]
        # authenticated user gists
        # api v3 authenticated user gists (`files` with `language` )
        url = "https://api.github.com/gists?user_id=%s&login=%s&per_page=100&page=1" % (github_user.id,github_user.login)
        url_list+=[url]
        # graphql viewer gists - `files` `language` not supported
        url = (
            "https://api.github.com/graphql?schema=viewer.gists&user_id=%s&login=%s&page=1"
            % (github_user.id,github_user.login)
        )
        url_list+=[url]
        url2query[url] = get_viewer_gists_query()
    else:  # public user
        # todo: etag. no need all requests if no changes. where to check?
        if github_user.public_gists_count:
            # &page=1 request only (etag check)
            url = "https://api.github.com/user/%s/gists?login=%s&per_page=100&page=%s" % (
                github_user.id,
                github_user.login,
                1,
            )
            url_list+=[url]
            # graphql user gists - `files` `language` not supported
            url = (
                "https://api.github.com/graphql?schema=user.gists&user_id=%slogin=%s" % (github_user.id,github_user.login,)
            )
            url_list+=[url]
            url2query[url] = get_user_gists_query(github_user.login)
    timestamp = round(time.time(),3)
    create_list = []
    for url in url_list:
        data = None
        if "github.com/graphql" in url:
            query = url2query[url]
            data = json.dumps({"query": query.replace("\n", "")})
            headers["Content-Type"] = "application/json"
        create_list += [
            RequestJob(
                host="api.github.com",
                url=url,
                method="GET" if "github.com/graphql" not in url else "POST",
                headers=json.dumps(headers),
                data=data,
                disk_path=get_disk_path(url),
                redirects_limit=4,
                retries_limit=5,
                timeout=10,
                priority=priority,
            ),
            GithubUserRefresh(
                user_id=request.user.id,
                github_user_id=github_user.id,
                started_at=timestamp
            ),
            GithubUserRefreshLock(
                user_id=request.user.id,
                github_user_id=github_user.id,
                created_at=timestamp
            )
        ]
    model2kwargs = {
        GithubUserRefresh:dict(ignore_conflicts=True),
        GithubUserRefreshLock:dict(ignore_conflicts=True),
    }
    with transaction.atomic():
        bulk_create(create_list,model2kwargs)
        Queue.objects.get_or_create(name='github_user_refresh_unlock')


def timesince(d):
    yesterday = date.today() - timedelta(days=1)
    td = datetime.now() - d
    td_seconds = td.total_seconds()
    td_hours = int(td_seconds / (60 * 60))
    if td.days == 0 and td.total_seconds() < 60:
        return "now"
    if td.days == 0 and not td_hours:
        return "%s ago" % _timesince(d).split(",")[0]
    if td.days == 0 and td.total_seconds() < 60 * 60 * 2:
        return "1 hour ago"
    if td.days == 0 or (d.date() == yesterday and td_hours <= 23):
        return "%s hours ago" % td_hours
    if d.date() == yesterday:
        return "yesterday"
    if td.days <= 31:
        return "%s days ago" % td.days
    return "%s ago" % _timesince(d).split(",")[0]
