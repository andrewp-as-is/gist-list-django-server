import collections
import time

from django.db.models import Count, Q

from base.apps.github.models import Language

from base.apps.github.models import Gist, GistLanguage, Trash
from base.apps.github_default_matview.models import Gist as DefaultGist, GistLanguage as DefaultGistLanguage
from base.apps.github_recent_matview.models import Gist as RecentGist, GistLanguage as RecentGistLanguage
from base.apps.tag.models import Tag

LANGUAGE_LIST = list(Language.objects.all())
TAG_LIST = list(Tag.objects.all())
ID2LANGUAGE = {language.id:language for language in LANGUAGE_LIST}
NAME2LANGUAGE = {language.name:language for language in LANGUAGE_LIST}
SLUG2LANGUAGE = {language.slug:language for language in LANGUAGE_LIST}
ID2TAG = {tag.id:tag for tag in TAG_LIST}
SLUG2TAG = {tag.slug:tag for tag in TAG_LIST}


def get_gist_model(user_stat):
    if not user_stat:
        return DefaultGist
    if not user_stat.refreshed_at or user_stat.refreshed_at+60>time.time():
        return Gist
    if user_stat.refreshed_at and user_stat.refreshed_at+3600*24>time.time():
        return RecentGist
    return DefaultGist

def get_gist_language_model(user_stat):
    if not user_stat:
        return DefaultGistLanguage
    if not user_stat.refreshed_at or user_stat.refreshed_at+60>time.time():
        return GistLanguage
    if user_stat.refreshed_at and user_stat.refreshed_at+3600*24>time.time():
        return RecentGistLanguage
    return DefaultGistLanguage

def get_object(model,**kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        pass

def get_language(value):
    if value in NAME2LANGUAGE:
        return NAME2LANGUAGE[value]
    if value in SLUG2LANGUAGE:
        return SLUG2LANGUAGE[value]

def get_tag(slug):
    if slug:
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            pass
