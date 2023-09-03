import collections

from base.apps.github.models import Language
from base.apps.tag.models import Tag

from views.utils import get_url

LANGUAGE_LIST = list(Language.objects.all())
TAG_LIST = list(Tag.objects.all())
ID2LANGUAGE = {language.id:language for language in LANGUAGE_LIST}
ID2TAG = {tag.id:tag for tag in TAG_LIST}
SLUG2TAG = {tag.slug:tag for tag in TAG_LIST}


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

def get_language(slug):
    if slug:
        try:
            return Language.objects.get(slug=slug)
        except Language.DoesNotExist:
            pass

def get_tag(slug):
    if slug:
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            pass

def get_language_filter(request,data):
    item_list = [dict(
        slug='',
        name='All',
        selected=request.GET.get('language','')=='',
        url= get_url(request,language='')
    )]
    if data.get(0,0)>0:
        item_list+=[dict(
            slug='none',
            name='NO LANGUAGE',
            selected=request.GET.get('language','')=='none',
            count=data.get(0,0),
            url= get_url(request,language='none',tag='')
        )]
    language_stat_list = []
    for language_id,count in data.items():
        language = ID2LANGUAGE.get(language_id,None)
        if language:
            language_stat_list+=[{
                'name':language.name,
                'slug':language.slug,
                'selected':request.GET.get('language','')==language.slug,
                'color':language.color,
                'count':count,
                'url': get_url(request,language=language.slug)
            }]
    item_list+=list(sorted(language_stat_list,key=lambda l:l['slug']))
    return dict(item_list=item_list)

def get_tag_filter(request,data):
    global ID2TAG
    item_list = [dict(
        slug='',
        name='All',
        selected=request.GET.get('tag','')=='',
        url= get_url(request,language='',tag='')
    )]
    if data.get(0,0)>0:
        item_list+=[dict(
            slug='none',
            name='NO TAGS',
            selected=request.GET.get('tag','')=='none',
            count=data.get(0,0),
            url= get_url(request,language='',tag='none')
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
                'name':'#'+tag.slug,
                'slug':tag.slug,
                'selected':request.GET.get('tag','')==tag.slug,
                'count':count,
                'url': get_url(request,language='',tag=tag.slug)
            }]

    item_list+=list(sorted(tag_stat_list,key=lambda l:l['slug']))
    return dict(item_list=item_list)
