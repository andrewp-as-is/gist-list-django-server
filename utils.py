import json
from datetime import date, datetime, timedelta
import os
import time

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils.timesince import timesince as _timesince
import requests

from base.apps.github_matview.models import Gist as MatviewGist
from base.apps.github_modification_matview.models import Gist as NewMatviewGist
from base.apps.github.models import GistRefreshLock, UserRefreshLock, UserRefreshViewer
from base.apps.github.utils.graphql import (
    get_user_followers_query,
    get_user_following_query,
    get_viewer_gists_query,
    get_user_gists_query,
)
from base.conf import HTTP_CLIENT_DIR

from base.apps.github.utils.http_response import (
    get_api_gists_gist_disk_path,
    get_api_user_gists_pagination_page_disk_path,
    get_api_viewer_gists_pagination_page_disk_path,
    get_api_viewer_gists_starred_pagination_page_disk_path,
    get_api_graphql_user_followers_pagination_page_disk_path,
    get_api_graphql_user_following_pagination_page_disk_path,
    get_api_graphql_viewer_gists_pagination_page_disk_path,
    get_api_graphql_user_gists_pagination_page_disk_path,
)
from django_bulk_create import bulk_create
from django_http_client.models import Request

REGCLASS2MODEL = {}


def get_model(schemaname, relname):
    global REGCLASS2MODEL
    regclass = '"%s"."%s"' % (schemaname, relname)
    model = REGCLASS2MODEL.get(regclass, None)
    if model:
        return model
    for model in filter(lambda m: "." in m._meta.db_table, apps.get_models()):
        db_table = model._meta.db_table.replace('"', "")
        _schemaname = db_table.split(".")[0].replace('"', "")
        _relname = db_table.split(".")[1].replace('"', "")
        if schemaname == _schemaname and relname == _relname:
            REGCLASS2MODEL[regclass] = model
            return model


def get_matview_model(expired_at, matviewname):
    schemaname = "github_matview"
    if (expired_at or 0) > int(time.time()) + 1:
        schemaname = "github_modification_matview"
    return get_model(schemaname, matviewname)


def get_follower_model(time):
    matviewname = "follower"
    expired_at = time.follower_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


def get_following_model(time):
    matviewname = "follower"
    expired_at = time.following_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


def get_gist_model(time):
    matviewname = "gist"
    expired_at = time.gist_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


def get_starred_gist_model(time):
    matviewname = "starred_gist"
    expired_at = time.gist_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


def get_gist_language_model(time):
    matviewname = "gist_language"
    expired_at = time.gist_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


def get_gist_tag_model(time):
    matviewname = "gist_tag"
    expired_at = time.gist_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


def get_user_model(time):
    matviewname = "user"
    expired_at = time.gist_expired_at if time else 0
    return get_matview_model(expired_at, matviewname)


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
    url2relpath = {}
    url2query = {}
    headers = {
        "Authorization": "Bearer %s" % token.token,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = "https://api.github.com/gists/%s" % gist.id
    url2relpath[url] = get_api_gists_gist_disk_path(gist.id)
    create_list = []
    for url, disk_path in url2relpath.items():
        data = None
        if "github.com/graphql" in url:
            query = url2query[url]
            data = json.dumps({"query": query.replace("\n", "")})
            headers["Content-Type"] = "application/json"
        print("url: %s" % url)
        print("headers: %s" % headers)
        print("data: %s" % data)
        create_list += [
            Request(
                host="api.github.com",
                url=url,
                method="GET" if "github.com/graphql" not in url else "POST",
                headers=json.dumps(headers),
                data=data,
                disk_path=disk_path,
                priority=priority,
            )
        ]
        create_list += [GistRefreshLock(gist_id=gist.id, timestamp=int(time.time()))]
    with transaction.atomic():
        bulk_create(create_list)


def refresh_user(user, token, priority, **options):
    # todo: priority based on user.id vs token.user_id
    # root = 'api.github.com/user/%s' % (user.id)
    url2relpath = {}
    url2query = {}
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
    url = "https://api.github.com/user/%s" % user.id
    url2relpath[url] = "api.github.com/user/%s/profile" % user.id
    # graphql user followers
    url = (
        "https://api.github.com/graphql?schema=user.followers&user_id=%s&page=1"
        % user.id
    )
    url2relpath[url] = get_api_graphql_user_followers_pagination_page_disk_path(
        user.id, 1
    )
    url2query[url] = get_user_followers_query(user.login)
    # graphql user following
    url = (
        "https://api.github.com/graphql?schema=user.following&user_id=%s&page=1"
        % user.id
    )
    url2relpath[url] = get_api_graphql_user_following_pagination_page_disk_path(
        user.id, 1
    )
    url2query[url] = get_user_following_query(user.login)
    secret = user.id == token.user_id
    if secret:  # authenticated user (unknown pages count)
        # gists/starred api v3 only, graphql not supported
        url = (
            "https://api.github.com/gists/starred?user_id=%s&per_page=100&page=1"
            % user.id
        )
        url2relpath[url] = get_api_viewer_gists_starred_pagination_page_disk_path(
            user.id, 1
        )
        # authenticated user gists
        # api v3 authenticated user gists (`files` with `language` )
        url = "https://api.github.com/gists?user_id=%s&per_page=100&page=1" % (user.id)
        url2relpath[url] = get_api_viewer_gists_pagination_page_disk_path(user.id, 1)
        # graphql viewer gists - `files` `language` not supported
        url = (
            "https://api.github.com/graphql?schema=viewer.gists&user_id=%s&page=1"
            % user.id
        )
        url2relpath[url] = get_api_graphql_viewer_gists_pagination_page_disk_path(
            user.id, 1
        )
        url2query[url] = get_viewer_gists_query()
    else:  # public user
        # todo: etag. no need all requests if no changes. where to check?
        if user.public_gists_count:
            # &page=1 request only (etag check)
            url = "https://api.github.com/user/%s/gists?per_page=100&page=%s" % (
                user.id,
                1,
            )
            url2relpath[url] = get_api_user_gists_pagination_page_disk_path(user.id, 1)
            # graphql user gists - `files` `language` not supported
            url = (
                "https://api.github.com/graphql?schema=user.gists&user_id=%s" % user.id
            )
            url2relpath[url] = get_api_graphql_user_gists_pagination_page_disk_path(
                user.id, 1
            )
            url2query[url] = get_user_gists_query(user.login)
    create_list = []
    for url, disk_disk_path in url2relpath.items():
        data = None
        if "github.com/graphql" in url:
            query = url2query[url]
            data = json.dumps({"query": query.replace("\n", "")})
            headers["Content-Type"] = "application/json"
        disk_path = os.path.join(HTTP_CLIENT_DIR, disk_disk_path)
        print("url: %s" % url)
        print("headers: %s" % headers)
        print("data: %s" % data)
        create_list += [
            Request(
                host="api.github.com",
                url=url,
                method="GET" if "github.com/graphql" not in url else "POST",
                headers=json.dumps(headers),
                data=data,
                disk_path=disk_path,
                priority=priority,
            )
        ]
        create_list += [
            UserRefreshLock(user_id=user.id, secret=secret, timestamp=int(time.time()))
        ]
        create_list += [
            UserRefreshViewer(
                user_id=user.id, viewer_id=token.user_id, timestamp=int(time.time())
            )
        ]
    with transaction.atomic():
        bulk_create(create_list)


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
