import collections

from django.db.models import Count, Q

from base.apps.github.models import Language

from base.apps.github.models import Gist, GistTrash
from base.apps.tag.models import Tag

LANGUAGE_LIST = list(Language.objects.all())
TAG_LIST = list(Tag.objects.all())
ID2LANGUAGE = {language.id:language for language in LANGUAGE_LIST}
NAME2LANGUAGE = {language.name:language for language in LANGUAGE_LIST}
SLUG2LANGUAGE = {language.slug:language for language in LANGUAGE_LIST}
ID2TAG = {tag.id:tag for tag in TAG_LIST}
SLUG2TAG = {tag.slug:tag for tag in TAG_LIST}



def get_language_stat(queryset,gist_language_model):
    print('gist_language_model: %s' % gist_language_model)
    gist_id_qs = queryset.values_list('id',flat=True)
    gist_delete_qs = GistTrash.objects.values_list('gist_id',flat=True)  # live gists only
    data = {r['language_id']:r['count'] for r in gist_language_model.objects.filter(
        gist__in=gist_id_qs
    ).values('language_id').annotate(count=Count('language_id'))}
    # NO LANGUAGE
    data[0] = queryset.exclude(
        id__in=gist_language_model.objects.filter(
            gist__in=gist_id_qs
        ).values_list('gist_id',flat=True)
    ).exclude(id__in=gist_delete_qs).count()
    return data


def get_tag_stat(queryset,gist_tag_model):
    gist_id_qs = queryset.values_list('id',flat=True)
    gist_delete_qs = GistTrash.objects.values_list('gist_id',flat=True)  # live gists only
    data = {r['tag_id']:r['count'] for r in gist_tag_model.objects.filter(
        gist__in=gist_id_qs
    ).values('tag_id').annotate(count=Count('tag_id'))}
    # NO TAGS
    data[0] = queryset.exclude(
        id__in=gist_tag_model.objects.filter(
            gist__in=gist_id_qs
        ).values_list('gist_id',flat=True)
    ).exclude(id__in=gist_delete_qs).count()
    return data

def get_stat_data(stat):
    data = {}
    for l in stat.stat.splitlines():
        data[int(l.split(':')[0])] = int(l.split(':')[1])
    return data


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

def get_language_item_list(data):
    item_list = [{
        'value':'',
        'text':'All'
    }]
    if data.get(0,0)>0:
        item_list+=[dict(
            value='none',
            text='NO LANGUAGE',
            count=data.get(0,0)
        )]
    language_stat_list = []
    for language_id,count in data.items():
        language = ID2LANGUAGE.get(language_id,None)
        if language:
            item_list+=[{
                'value':language.slug,
                'text':language.name,
                'count':count
            }]
    item_list+=list(sorted(language_stat_list,key=lambda l:l['count']))
    return item_list

def get_tag_item_list(data):
    item_list = [dict(
        value='',
        text='All'
    )]
    if data.get(0,0)>0:
        item_list+=[dict(
            value='none',
            text='NO TAGS',
            count = data.get(0,0)
        )]
    tag_stat_list = []
    for tag_id,count in data.items():
        if tag_id>0:
            tag = ID2TAG.get(tag_id,None)
            if not tag:
                try:
                    tag = Tag.objects.get(id=tag_id)
                except Tag.DoesNotExist:
                    continue
            tag_stat_list+=[{
                'text':'#'+tag.slug,
                'value':tag.slug,
                'count':count
            }]
    item_list+=list(sorted(tag_stat_list,key=lambda l:l['value']))
    return item_list
