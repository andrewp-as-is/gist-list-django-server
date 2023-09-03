from datetime import datetime

from base_apps.utils import get_tags


from base_apps.github.models import Gist #, GistLanguage

def get_kwargs(data):
    return dict(
        description = data['description'],
        filename = list(data['files'].keys())[0],
        files_count = len(data['files']),
        files = ','.join(sorted(map(lambda s:s.lower(),data['files']))),
        updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
    )

def sync_languages(data):
    gist_id = data['id']
    gist_language_list = list(GistLanguage.objects.filter(gist_id=gist_id))
    names = list(sorted(set(filter(None,
        map(lambda f:f['language'],data['files'].values())
    ))))
    for name in names:
        slug = name.lower()
        defaults = dict(name=name)
        Language.objects.get_or_create(defaults,slug=slug)
    slugs = list(map(lambda s:s.lower(),names))
    _gist_language_list = list(filter(lambda gl:gl.gist_id==gist_id,gist_language_list))
    new_slugs = list(set(slugs)-set(map(lambda gl:gl.slug,_gist_language_list)))
    for slug in new_slugs:
        django_bulk.create(GistLanguage(gist_id=gist_id,slug=slug))
    for gl in _gist_language_list:
        if gl.slug not in slugs:
            django_bulk.delete(gl)

def sync_tags(data):
    gist_id = data['id']
    gist_tag_list = list(GistTag.objects.filter(gist_id=gist_id))
    # UpperCase allowed (user tags only, not global)
    slugs = get_tags(data['description'] or '')
    _gist_tag_list = list(filter(lambda gt:gt.gist_id==gist_id,gist_tag_list))
    new_slugs = list(set(slugs)-set(map(lambda gl:gl.slug,_gist_tag_list)))
    for slug in new_slugs:
        django_bulk.create(GistTag(gist_id=gist_id,slug=slug))
    for gl in _gist_tag_list:
        if gl.slug not in slugs:
            django_bulk.delete(gl)

def sync_gist(data):
    sync_languages(data)
    sync_tags(data)
    django_bulk.execute()
