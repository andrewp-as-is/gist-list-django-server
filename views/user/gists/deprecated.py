from django.db.models import Count, F, Q
from django.db.models.functions import Lower
from django.db.models.query import Prefetch
from django.shortcuts import redirect

from base.apps.github.models import Gist #, GistLanguage
from base.apps.github_gist_matview.models import Gist
from base.apps.github.models import Language, User
from views.base import ListView
from views.user.mixins import UserMixin
from .utils import get_language_list

LANGUAGE_LIST = list(Language.objects.all())


class ListView(UserMixin,ListView):
    context_object_name = "gist_list"
    template_name = "user/gists/gist_list.html"
    public = None

    def get_model(self):
        return Gist

    def get(self,request,*args,**kwargs):
        login = self.kwargs.get('login')
        if request.path == '/%s/' % login:
            return redirect('/%s' % login)
        return super().get(request,*args,**kwargs)

    def get_paginate_by(self,request):
        value = self.request.GET.get('v','')
        if value and value.isdigit() and value in ['10','100','1000','10000']:
            return int(value)
        return 100

    def get_url(self,**kwargs):
        data = {k:v for k,v in self.request.GET.items()}
        data.update(kwargs)
        params = []
        for k in list(data.keys()):
            params.append('%s=%s' % (k,data[k]))
        return self.request.path+'?'+'&'.join(params)

    def get_column_list(self):
        column_list = [
            {'key':'download','name':'Download'},
            {'key':'id','name':'ID'},
            {'key':'name','name':'Name'},
            {'key':'description','name':'Description'},
            {'key':'tags','name':'Tags'},
            {'key':'languages','name':'Languages'},
            {'key':'files','name':'Files'},
            {'key':'stars','name':'Stars'},
            {'key':'forks','name':'Forks'},
            {'key':'comments','name':'Comments'},
            {'key':'committed','name':'Committed'}
        ]
        keys = list(map(lambda c:c['key'],filter(lambda c:c['key'],column_list)))
        default_keys = list(filter(
            lambda k:k in ['name','description','tags','languages','files','stars','forks','comments','committed',]+[self.request.GET.get('sort','')],
            list(map(lambda c:c['key'],column_list))
        ))
        value = self.request.GET.get('columns','') or ','.join(default_keys)
        if len(set(value.split(',')))!=len(column_list):
            column_list = [{'key':'','name':'All','url':self.get_url(columns=','.join(keys))}]+column_list
        for l in column_list:
            l['selected'] = l['key'] in value if l['key'] else False
            columns = value
            if l['selected']:
                columns = ','.join(filter(lambda c:c!=l['key'],value.split(',')))
            else:
                columns = []
                for c in column_list:
                    if c['key'] and (c['key'] in value or l['key']==c['key']):
                        columns.append(c['key'])
                columns = ','.join(columns)
            if not l['key']:
                columns = ','.join(keys)
            l['url'] = self.get_url(columns=columns)
        return column_list


    def get_sort_list(self):
        value = self.request.GET.get('sort','')
        default_value = ''
        item_list = [
            {'key':'id','name':'ID'},
            {'key':'name','name':'Name'},
            {'key':'description','name':'Description'},
            {'key':'files','name':'Files'},
            #{'key':'stars','name':'Stars'},
           # {'key':'forks','name':'Forks'},
            {'key':'comments','name':'Comments'},
            {'key':'created','name':'Last created'},
            {'key':'','name':'Last commited'},
        ]
        for i in item_list:
            i['selected'] = i['key'] == value or (value=='' and i['key']==default_value)
            i['url'] = self.get_url(sort=i['key'])
        return item_list

    def get_tag_list(self):
        prefix = 'gist__' if self.request.path.split('/')[-1] == 'starred' else ''
        value = self.request.GET.get('tag','')
        return []
        qs = GistTag.objects.filter(
            gist_id__in=self.get_queryset_base().values_list(prefix+'id',flat=True)
        ).values('slug').annotate(
            key = F('slug'),
            name = F('slug'),
            count=Count('slug')
        ).order_by('slug').all()
        tag_list = [dict(slug='',key='',name='All')]+list(qs)
        for l in tag_list:
            l['selected'] = l['key'] == value
            l['url'] = self.get_url(tag=l['slug'])
        return tag_list

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

    def get_view_list(self):
        value = self.request.GET.get('v','')
        default_value = '100'
        item_list = [
            {'key':'10','name':'10'},
            {'key':'100','name':'100'},
            {'key':'1000','name':'1000'},
            {'key':'10000','name':'10000'},
        ]
        for i in item_list:
            i['selected'] = i['key'] == value or (value=='' and i['key']==default_value)
            i['url'] = self.get_url(v=i['key'])
        return item_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.github_user:
            is_owner = self.request.user.is_authenticated and self.request.user.login == self.github_user.login
            if is_owner:
                context['blankslate'] = not self.github_user.public_gists_count and not self.github_user.private_gists_count
            else:
                context['blankslate'] = not self.github_user.public_gists_count
            # context['user_language_list'] = list(GistLanguage.objects.filter(user=self.github_user).order_by('slug'))
            column_list = self.get_column_list()
            context['columns'] = list(map(lambda c:c['key'],filter(lambda c:c['selected'],column_list)))
            context['details'] = self.get_details()
            context['language_list'] = get_language_list(self.request,self.github_user.id)
        return context

    def get_details(self):
        return {
            'sort':{'item_list':self.get_sort_list()},
            'columns':{'item_list':self.get_column_list()},
             #'type':{'item_list':self.get_details_type_item_list()},
            'view':{'item_list':self.get_view_list()},
        }

    def get_queryset_base(self):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        qs = model.objects.filter(owner_id=self.github_user.id)
        if not self.request.user.is_authenticated or self.github_user.login != self.request.user.login:
            qs = qs.filter(public=True)
        return qs

    def get_queryset(self,**kwargs):
        prefix = 'gist__' if self.request.path.split('/')[-1] == 'starred' else ''
        #queryset = GistLanguage.objects.filter(
       #     gist_id__in=Gist.objects.filter(#owner_id=self.github_user.id).values_list('id',flat=True)
       # )
        # prefetch = Prefetch("gist_language_set", queryset=queryset, to_attr='gist_language_list')

        qs = self.get_queryset_base()# .prefetch_related(prefetch)
        language_slug = self.request.GET.get('language','').strip().lower()
        language = next(filter(lambda l:l.slug==language_slug,LANGUAGE_LIST),None)
        if language and 1==2:
            kwargs = {
                prefix+'id__in':GistLanguage.objects.filter(
                    language_id=language.id,
                    gist_id__in=Gist.objects.filter(owner_id=self.github_user.id).values_list('id',flat=True),
                ).values_list('gist_id',flat=True)
            }
            qs = qs.filter(**kwargs)
        tag_slug = self.request.GET.get('tag','').strip().lower()
        tag = get_tag(self.request.GET.get('tag','').strip().lower())
        if tag:
            kwargs = {prefix+'id__in':GistTag.objects.filter(
                tag_id=tag.id,
                gist_id__in=Gist.objects.filter(owner_id=self.github_user.id).values_list('id',flat=True)
                ).values_list('gist_id',flat=True)}
            qs = qs.filter(**kwargs)
        #if q:
        #    qs = qs.filter(language__icontains=language.lower())
        kwargs = {}
        qs = qs.filter(**kwargs)
        q = self.request.GET.get('q','').strip()
        if q:
            qs = qs.filter(
                Q(**{prefix+'id__icontains':q}) |
                Q(**{prefix+'description__icontains':q}) |
                Q(**{prefix+'files__icontains':q}) |
                Q(**{prefix+'languages__icontains':q})
            )
        order_by = ['-%screated_at' % prefix]
        sort = self.request.GET.get('sort','')
        if self.request.path.split('/')[-1] == '/starred':
            order_by = ['-starred_order']
        if sort == 'created':
            order_by = ['-%screated_at' % prefix]
        if sort == 'committed':
            order_by = ['-%scommitted_at' % prefix]
        if sort == 'description':
            order_by = [Lower(prefix+'description'),prefix+'id']
            print(order_by)
        if sort == 'name':
            order_by = [Lower(prefix+'filename'),prefix+'id']
        if sort == 'stars':
            order_by = [F(prefix+'stargazers_count').desc(nulls_last=True),prefix+'id']
        if sort == 'forks':
            order_by = [F(prefix+'forks_count').desc(nulls_last=True),prefix+'id']
        if sort == 'comments':
            order_by = [F(prefix+'comments_count').desc(nulls_last=True),prefix+'id']
        if sort == 'id':
            order_by = [prefix+'id']
        qs = qs.order_by(*order_by)
        if self.request.path.split('/')[-1] == '/starred':
            qs = qs.select_related(prefix+'owner')
        return qs
