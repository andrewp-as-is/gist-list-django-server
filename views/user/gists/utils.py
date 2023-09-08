import collections

from django.db.models import Count, Q

from base.apps.github.models import Language

from base.apps.github.models import Gist, GistDelete
from base.apps.tag.models import Tag

from views.utils import get_gist_model, get_url

LANGUAGE_LIST = list(Language.objects.all())
TAG_LIST = list(Tag.objects.all())
ID2LANGUAGE = {language.id:language for language in LANGUAGE_LIST}
ID2TAG = {tag.id:tag for tag in TAG_LIST}
SLUG2TAG = {tag.slug:tag for tag in TAG_LIST}


def get_queryset_base(request,github_user):
    model = get_gist_model(github_user.id)
    qs = model.objects.filter(owner_id=github_user.id)
    if not request.user.is_authenticated or github_user.login != request.user.login:
        qs = qs.filter(public=True)
    return qs

def get_language_stat(queryset,gist_language_model):
    gist_id_qs = queryset.values_list('id',flat=True)
    gist_delete_qs = GistDelete.objects.values_list('gist_id',flat=True)  # live gists only
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
    gist_delete_qs = GistDelete.objects.values_list('gist_id',flat=True)  # live gists only
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
