import time

from base.apps.github.models import Gist, GistMatview, GistStar, GistStarMatview, Language, Trash
from base.apps.github.models import GistMatview #, GistStarInfoMatview
# from base.apps.github_recent_matview.models import Gist as RecentGist, StarredGist as RecentStarredGist

LANGUAGE_NAME2COLOR = {l.name:l.color for l in Language.objects.all()}

def get_language_list(user_stat,secret):
    language_list = []
    if user_stat:
        text_stat = user_stat.public_language_stat
        gists_count = user_stat.public_gists_count
        if secret:
            gists_count+=user_stat.secret_gists_count
            text_stat = user_stat.secret_language_stat
        data = get_stat_data(text_stat)
        sorted_data = {r: data[r] for r in sorted(data, key=data.get, reverse=True)}
        for name,count in sorted_data.items():
            percent = None
            if len(data)>1:
                percent = round(100 * float(count)/gists_count,1)
            color= LANGUAGE_NAME2COLOR.get(name,None)
            language_list+=[dict(name=name,color=color,count=count,percent=percent)]
    return language_list


def get_tag_list(user_stat,secret):
    tag_list = []
    text_stat = user_stat.public_tag_stat
    gists_count = user_stat.public_gists_count
    if secret:
        gists_count+=user_stat.secret_gists_count
        text_stat = user_stat.secret_tag_stat
    data = get_stat_data(text_stat)
    sorted_data = {r: data[r] for r in sorted(data, key=data.get, reverse=True)}
    for slug,count in sorted_data.items():
        percent = None
        if len(data)>1:
            percent = round(100 * float(count)/gists_count,1)
        tag_list+=[dict(slug=slug,count=count,percent=percent)]
    return tag_list




def get_stat_data(stat):
    data = {}
    if stat:
        for l in stat.splitlines():
            data[l.split(':')[0]] = l.split(':')[1].strip()
    return data

def get_gist_model(user_stat):
    # todo: VacuumFullLock
    if not user_stat:
        return Gist
    return GistMatview
    if not user_stat.user_refreshed_at or user_stat.user_refreshed_at+60>time.time():
        return Gist
    if user_stat.user_refreshed_at and user_stat.user_refreshed_at+3600*24>time.time():
        return RecentGist
    return GistMatview

def get_gist_star_model(user_stat):
    return GistStar
    # todo: models
    if not user_stat:
        return
    if not user_stat.user_refreshed_at or user_stat.user_refreshed_at+3600*24>time.time():
        return GistStar
    return GistStarMatview
