import time

from base.apps.github_default_matview.models import GistStar as DefaultGistStar, StarredGist as DefaultStarredGist
from base.apps.github_recent_matview.models import GistStar as RecentGistStar, StarredGist as RecentStarredGist

def get_gist_star_model(user_stat):
    if not user_stat:
        return
    if not user_stat.refreshed_at or user_stat.refreshed_at+3600*24>time.time():
        return RecentGistStar
    return DefaultGistStar

def get_starred_gist_model(user_stat):
    if not user_stat:
        return
    if not user_stat.refreshed_at or user_stat.refreshed_at+3600*24>time.time():
        return RecentStarredGist
    return DefaultStarredGist
