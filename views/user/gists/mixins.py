from django.http import HttpResponse


class CloneMixin:
    paginate_by = 100000
    template_name = "user/clone/clone.html"

    def get_paginate_by(self, request):
        return 100000

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        gists_count = len(list(self.get_queryset().only('id')))
        clone_filename = 'gists-clone.sh'
        if '/public/clone' in self.request.path:
            clone_filename = 'gists-public-clone.sh'
        if '/secret/clone' in self.request.path:
            clone_filename = 'gists-secret-clone.sh'
        context_data['clone_filename'] = 'gists_clone.sh'
        context_data['textarea'] = dict(rows=2+3*gists_count)
        context['context_data'] = context_data
        return context


    def get_type_menu_item_list(self):
        public_selected = '/public/clone' in self.request.path
        secret_selected = '/secret/clone' in self.request.path
        all_selected = not public_selected and not secret_selected
        protocol = self.request.GET.get('protocol','') or 'ssh'
        if self.github_user:
            url = self.github_user.get_absolute_url()+'/gists'
            url_postfix='/clone?protocol=%s' % protocol
            return [
                {'description':'All','url':url+url_postfix,'selected':all_selected},
                {'description':'Public','url':url+'/public'+url_postfix,'selected':public_selected},
                {'description':'Secret','url':url+'/secret'+url_postfix,'selected':secret_selected},
            ]


class CloneShMixin:
    paginate_by = 100000

    def get_paginate_by(self, request):
        return 100000

    def get(self, request, *args, **kwargs):
        protocol = self.request.GET.get('protocol','ssh') or 'ssh'
        print('get_paginate_by: %s' % self.get_paginate_by(self.request))
        gist_list = list(self.get_queryset().order_by('id'))
        clone_list = []
        for gist in gist_list:
            clone_list+=["""[ -e %s ] || {
  ( set -x; git clone -q git@gist.github.com:%s.git ) || exit
}""" % (gist.id,gist.id)]
        content = """#!/bin/sh

%s
""" % "\n".join(clone_list)
        response = HttpResponse(content,content_type="text/plain")
        return response
