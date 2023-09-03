from django.apps import apps
from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import redirect

from base.apps.github.models import Gist, GistDelete, GistTag, GistLanguage, User
from views.base import ListView
from views.user.mixins import UserMixin
from views.utils import get_gist_model
from .utils import get_object, get_language, get_language_filter, get_tag_filter, get_tag
from . import details

class ListView(UserMixin,ListView):
    context_object_name = "gist_list"
    template_name = "user/gists/gist_list.html"
    public = None
    paginate_by = 100

    def get_model(self):
        user_id = self.github_user.id if self.github_user else None
        return get_gist_model(user_id)

    def iter_app_model(self):
        gist_model = self.get_model()
        for model in apps.get_models():
            if model._meta.app_label==gist_model._meta.app_label:
                yield model

    def get_gist_language_model(self):
        for model in self.iter_app_model():
            if 'language' in model.__name__.lower():
                return model

    def get_gist_tag_model(self):
        for model in self.iter_app_model():
            if 'tag' in model.__name__.lower():
                return model

    def get(self,request,*args,**kwargs):
        login = self.kwargs.get('login')
        if request.path == '/%s/' % login:
            return redirect('/%s' % login)
        return super().get(request,*args,**kwargs)

    def get_paginate_by(self,request):
        value = self.request.GET.get('v','')
        if value and value.isdigit() and value in ['10','100','1000','10000']:
            return int(value)
        return self.paginate_by

    def get_url(self,**kwargs):
        data = {k:v for k,v in self.request.GET.items()}
        data.update(kwargs)
        params = []
        for k in list(data.keys()):
            params.append('%s=%s' % (k,data[k]))
        return self.request.path+'?'+'&'.join(params)

    def get_type_list(self):
        value = self.request.GET.get('type','')
        default_value = ''
        item_list = [{'key':'','name':'All','count':''},]
        if self.request.user.is_authenticated and self.github_user.login==self.request.user.login:
            if self.github_user.public_gists_count and self.github_user.private_gists_count:
                item_list+= [
                    {'key':'public','name':'Public','count':self.github_user.public_gists_count}
                ]
            if self.github_user.private_gists_count:
                item_list+= [
                    {'key':'private','name':'Private','count':self.github_user.private_gists_count},
                ]
        for i in item_list:
            i['selected'] = i['key'] == value or (value=='' and i['key']==default_value)
            i['url'] = self.get_url(type=i['key'])
        return item_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.github_user:
            user_id = self.github_user.id
            is_owner = self.request.user.is_authenticated and self.request.user.login == self.github_user.login
            if is_owner:
                context['blankslate'] = not self.github_user.public_gists_count and not self.github_user.private_gists_count
            else:
                context['blankslate'] = not self.github_user.public_gists_count
            context['details'] = self.get_details()
            gist_language_model = self.get_gist_language_model()
            gist_tag_model = self.get_gist_tag_model()
            count = self.get_queryset_base().count()
            context['queryset_count'] = count
            if count:
                gist_id_qs = self.get_queryset_base().values_list('id',flat=True)
                gist_delete_qs = GistDelete.objects.values_list('gist_id',flat=True)  # live gists only
                language_stat = {r['language_id']:r['count'] for r in gist_language_model.objects.filter(
                    gist__in=gist_id_qs
                ).values('language_id').annotate(count=Count('language_id'))}
                # NO LANGUAGE
                language_stat[0] = self.get_queryset_base().exclude(
                    id__in=gist_language_model.objects.filter(
                        gist__in=gist_id_qs
                    ).values_list('gist_id',flat=True)
                ).exclude(id__in=gist_delete_qs).count()
                tag_stat = {r['tag_id']:r['count'] for r in gist_tag_model.objects.filter(
                    gist__in=gist_id_qs
                ).values('tag_id').annotate(count=Count('tag_id'))}
                # NO TAGS
                tag_stat[0] = self.get_queryset_base().exclude(
                    id__in=gist_tag_model.objects.filter(
                        gist__in=gist_id_qs
                    ).values_list('gist_id',flat=True)
                ).exclude(id__in=gist_delete_qs).count()
                context['language_filter'] = get_language_filter(self.request,language_stat)
                context['tag_filter'] = get_tag_filter(self.request,tag_stat)
        return context

    def get_details(self):
        return {
            'sort':details.Sort(self.request),
            'view':details.View(self.request),
        }

    def get_queryset_base(self):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user or not self.refresh_time:
            return model.objects.none()
        qs = model.objects.filter(owner_id=self.github_user.id)
        if not self.request.user.is_authenticated or self.github_user.login != self.request.user.login:
            qs = qs.filter(public=True)
        return qs

    def get_queryset(self,**kwargs):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user or not self.refresh_time:
            return model.objects.none()
        prefix = 'gist__' if self.request.path.split('/')[-1] == 'starred' else ''
        qs = self.get_queryset_base()
        qs = qs.exclude(
            id__in=GistDelete.objects.values_list('gist_id',flat=True)
        ) # live gists only
        language_slug = self.request.GET.get('language','').strip().lower()
        language = get_language(language_slug)
        if language_slug:
            if language:
                qs = qs.filter(
                    id__in=GistLanguage.objects.filter(
                        language_id=language.id
                    ).values_list('gist_id',flat=True)
                )
            else:
                qs = qs.filter(language_m2m=None)
        tag_slug = self.request.GET.get('tag','').strip().lower()
        if tag_slug:
            tag = get_tag(tag_slug)
            if tag:
                pass
                #qs = qs.filter(
                #    id__in=GistTag.objects.filter(
                #        tag_id=tag.id
                #    ).values_list('gist_id',flat=True)
                #)
            else:
                qs = qs.filter(tag_m2m=None)
        q = self.request.GET.get('q','').strip()
        if q:
            qs = qs.filter(
                Q(**{'id__icontains':q}) |
                Q(**{'description__icontains':q}) |
                Q(**{'filenames__icontains':q})
                # Q(**{'languages__icontains':q})
            )
        sort = self.request.GET.get('sort','')
        sort_prefix = '-' if sort and sort[0]=='-' else ''
        sort_column = self.request.GET.get('sort','').replace('-','')
        order_by = ['created_order']
        if hasattr(model,'starred_order'):
            order_by = ['starred_order']
        if hasattr(model,'%s_order' % sort_column):
            order_by = [sort_prefix+'%s_order' % sort_column]
        if settings.DEBUG:
            print('order_by: %s' % order_by)
        qs = qs.order_by(*order_by)
        if hasattr(model,'starred_order'):
            qs = qs.select_related('owner')
        return qs
