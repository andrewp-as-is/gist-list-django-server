import time
from django.db import transaction
import requests

from base.apps.github_user_refresh.models import Lock
from base.apps.http_request_job.models import Job as RequestJob
from base.utils import bulk_create


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
    root = 'api.github.com/user/%s' % (user.id)
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
    url = 'https://api.github.com/graphql?schema=followers&user_id=%s' % user.id
    url2relpath[url] = 'graphql/followers/1'
    url2query[url] = """
query {
  user(login: "%s") {
    followers(first: 100) {
      nodes {
        databaseId
        login
        email
        name
        bio
        company
        location
        websiteUrl
        gists {
          totalCount
        }
        followers {
          totalCount
        }
        following {
          totalCount
        }
        twitterUsername
        createdAt
        updatedAt
      }
      pageInfo {
        endCursor
      }
    }
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
""" % user.login
    url = 'https://api.github.com/graphql?schema=following&user_id=%s' % user.id
    url2relpath[url] = 'graphql/following/1'
    url2data[url] = """
query {
  user(login: "%s") {
    following(first: 100) {
      nodes {
        databaseId
        login
        email
        name
        bio
        company
        location
        websiteUrl
        gists {
          totalCount
        }
        followers {
          totalCount
        }
        following {
          totalCount
        }
        twitterUsername
        createdAt
        updatedAt
      }
      pageInfo {
        endCursor
      }
    }
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
""" % user.login
    if user.id==token.user_id: # authenticated user (unknown pages count)
        url = 'https://api.github.com/gists?user_id=%s&per_page=100&page=1' % (user.id)
        url2relpath[url] = 'gists/1'
        url = 'https://api.github.com/gists/starred?user_id=%s&per_page=100&page=1' % user.id
        url2relpath[url] = 'gists-starred/1'
    else:
        url = 'https://api.github.com/user/%s' % user.id
        url2relpath[url] = 'user'
        if user.public_gists_count:
            for page in range(1,int(user.public_gists_count/100)+2):
                url = 'https://api.github.com/user/%s/gists?per_page=100&page=%s' % (user.id,page)
                url2relpath[url] = 'gists/%s' % page
    create_list = []
    for url,relpath in url2relpath.items():
        response_relpath = '%s/%s' % (root,relpath)
        headers = "\n".join([
            "Authorization: Bearer %s" % token.token,
            "X-GitHub-Api-Version: 2022-11-28"
        ])
        create_list+=[RequestJob(
            domain = 'api.github.com',
            url = url,
            method='GET' if 'github.com/graphql' not in url else 'POST',
            headers=headers,
            data = url2query.get(url,None),
            response_relpath=response_relpath,
            priority=priority if '/follow' not in url else 10,
            attempts_limit=5
        )]
    with transaction.atomic():
        defaults = dict(token_id=token.id,timestamp=int(time.time()))
        lock, created = Lock.objects.get_or_create(defaults,user_id=user.id)
        RequestJob.objects.bulk_create(create_list,ignore_conflicts=True)
