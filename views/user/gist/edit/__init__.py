from datetime import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

import requests

from base.apps.github.models import Gist, Token
from views.user.gist.mixins import GistMixin
# from utils import get_kwargs, sync_gist

"""
https://docs.github.com/en/rest/reference/gists#update-a-gist
"""

class EditView(LoginRequiredMixin,GistMixin,TemplateView):
    template_name = 'user/gist/edit/edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = Gist.objects.get(pk=self.kwargs['pk'])
        if self.object.owner_id != self.request.user.id:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = Token.objects.get(user_id=self.request.user.id)
        context['gist'] = self.object
        url = 'https://api.github.com/gists/%s' % self.kwargs['pk']
        headers = {"Authorization": "Bearer %s" % token.token}
        r = requests.get(url,headers=headers)
        # token.update(r.headers)
        if r.status_code in [200]:
            data = r.json()
            context['files'] = {f: data['content'] for f,data in data['files'].items()}
            context['old_names'] = ','.join(list(data['files'].keys()))
        return context

    def post(self, request,*args,**kwargs):
        gist_id = self.gist.id
        token = Token.objects.get(user_id=self.request.user.id)
        gist = Gist.objects.get(pk=gist_id)
        description = request.POST.get('gist[description]')
        names = request.POST.getlist('gist[contents][][name]')
        new_names = request.POST.getlist('gist[contents][][new_name]')
        values = request.POST.getlist('gist[contents][][value]')
        files = {name: None for name in request.POST['old_names'].split(',')}
        for i,name in enumerate(names):
            files[name] = dict(content = values[i],filename = new_names[i])
        url = 'https://api.github.com/gists/%s' % self.gist.id
        headers = {"Authorization": "Bearer %s" % token.token}
        data = dict(description = description,files = files)
        r = requests.patch(url,headers=headers,data=json.dumps(data))
        r.raise_for_status()
        if r.status_code in [200,204]:
            data = r.json()
            Gist.objects.filter(pk=gist_id).update(**get_kwargs(data))
            sync_gist(data)
        return redirect(gist.get_absolute_url())
