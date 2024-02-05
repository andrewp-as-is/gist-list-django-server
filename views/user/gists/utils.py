import collections
import time

from django.db.models import Count, Q

from base.apps.github.models import Language

LANGUAGE_LIST = list(Language.objects.all())
ID2LANGUAGE = {language.id:language for language in LANGUAGE_LIST}
NAME2LANGUAGE = {language.name:language for language in LANGUAGE_LIST}
SLUG2LANGUAGE = {language.slug:language for language in LANGUAGE_LIST}


def get_language(value):
    if value in NAME2LANGUAGE:
        return NAME2LANGUAGE[value]
    if value in SLUG2LANGUAGE:
        return SLUG2LANGUAGE[value]
