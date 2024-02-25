import json
from datetime import date, datetime, timedelta
import os
import time

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils.timesince import timesince as _timesince
import requests

from base.apps.django_command_worker.models import Queue
from base.apps.github.models import UserApiEtag, UserPublicStat, AuthenticatedUserStat
from base.apps.github.utils.graphql import (
    get_user_followers_query,
    get_user_following_query,
    get_viewer_gists_query,
    get_user_gists_query,
)

from base.apps.github.utils.http_response import get_disk_relpath
from base.apps.http_client.models import Request
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
            Request(
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
    url_list = []
    url2query = {}
    url2disk_relpath = {}
    token = request.user.token
    secret = github_user.id == token.user_id
    headers = {
        "Authorization": "Bearer %s" % token.token,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = "https://api.github.com/user/%s" % github_user.id
    url_list+=[url]
    # graphql user followers PROFILE
    url = (
        "https://api.github.com/graphql?schema=user.followers&page=1&user_id=%s"
        % (github_user.id)
    )
    url = "https://api.github.com/graphql"
    url_list+=[url]
    url2query[url] = get_user_followers_query(github_user.login)
    url2disk_relpath[url] = os.path.join('user',str(github_user.id),'graphql','followers','1')
    # graphql user following
    url = (
        "https://api.github.com/graphql?schema=user.following&page=1&user_id=%s"
        % (github_user.id)
    )
    url = "https://api.github.com/graphql"
    url_list+=[url]
    url2query[url] = get_user_following_query(github_user.login)
    url2disk_relpath[url] = os.path.join('user',str(github_user.id),'graphql','following','1')
    if secret:  # authenticated user (unknown pages count)
        # gists/starred api v3 only, graphql not supported
        url = (
            "https://api.github.com/gists/starred?per_page=100&page=1&user_id=%s"
            % (github_user.id)
        )
        url_list+=[url]
        # authenticated user gists
        # api v3 authenticated user gists (`files` with `language` )
        url = "https://api.github.com/gists?per_page=100&page=1&user_id=%s" % github_user.id
        url_list+=[url]
        # graphql viewer gists - `files` `language` not supported
        url = "https://api.github.com/graphql?schema=viewer.gists&page=1&user_id=%s" % github_user.id
        url_list+=[url]
        url2query[url] = get_viewer_gists_query()
    else:  # public user
        # todo: etag. no need all requests if no changes. where to check?
        if github_user.gists_count:
            # &page=1 request only (etag check)
            url = "https://api.github.com/user/%s/gists?per_page=100&page=1" % github_user.id
            url_list+=[url]
            # graphql user gists - `files` `language` not supported
            url = "https://api.github.com/graphql?schema=user.gists&page=1&user_id=%s" % github_user.id
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
            #if url in url2etag:
            #    headers["Etag"] = url2etag[url]
        if url in url2disk_relpath:
            disk_relpath = url2disk_relpath[url]
        else:
            disk_relpath = get_disk_relpath(url)
        if '?' not in url:
            url=url+'?'
        key2value = dict(
            user_id=github_user.id,
            token_id=token.id,
            login=github_user.login,
            priority=priority
        )
        for key,value in key2value.items():
            if key not in url:
                url=url+'&%s=%s' % (key,value)
        create_list += [
            Request(
                host="api.github.com",
                url=url,
                method="GET" if "github.com/graphql" not in url else "POST",
                headers=json.dumps(headers),
                data=data,
                disk_relpath=disk_relpath,
                max_redirects=4,
                max_retries=5,
                timeout=10,
                priority=priority,
            ),
        ]
    model2kwargs = {
        Request:dict(ignore_conflicts=True),
    }
    has_user_public_stat = bool(UserPublicStat.objects.filter(user_id=github_user.id).count()>0)
    UserPublicStat.objects.get_or_create(user_id=github_user.id)
    AuthenticatedUserStat.objects.get_or_create(user_id=github_user.id)
    with transaction.atomic():
        UserPublicStat.objects.filter(user_id=github_user.id).update(locked_at=timestamp)
        if secret:
            AuthenticatedUserStat.objects.filter(user_id=github_user.id).update(locked_at=timestamp)
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
