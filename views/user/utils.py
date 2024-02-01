from base.apps.github.models import Gist, Trash
from base.apps.github_default_matview.models import Gist as DefaultGist, GistStar as DefaultGistStar, StarredGist as DefaultStarredGist
from base.apps.github_recent_matview.models import Gist as RecentGist, GistStar as RecentGistStar, StarredGist as RecentStarredGist

def get_stat_data(stat):
    data = {}
    if stat:
        for l in stat.splitlines():
            data[l.split(':')[0]] = l.split(':')[1].strip()
    return data

def get_gist_model(user_stat):
    if not user_stat:
        return DefaultGist
    if not user_stat.refreshed_at or user_stat.refreshed_at+60>time.time():
        return Gist
    if user_stat.refreshed_at and user_stat.refreshed_at+3600*24>time.time():
        return RecentGist
    return DefaultGist

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
