#!/usr/bin/env python
from datetime import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

import requests

from base.apps.github.models import Gist
from django.views.generic.base import TemplateView

class GistUpdateView(LoginRequiredMixin,TemplateView):
    template_name = 'user/gist_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = Gist.objects.get(pk=self.kwargs['pk'])
        if self.object.owner_id != self.request.user.id:
            return redirect('/')
        return super(GistUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gist'] = self.object
        url = 'https://api.github.com/gists/%s' % self.kwargs['pk']
        headers = {"Authorization": "Bearer %s" % self.request.user.token}
        r = requests.get(url,headers=headers)
        data = r.json()
        context['files'] = {f: data['content'] for f,data in data['files'].items()}
        context['old_names'] = ','.join(list(data['files'].keys()))
        return context

    def post(self, request,login,pk):
        gist = Gist.objects.get(pk=pk)
        description = request.POST.get('gist[description]')
        names = request.POST.getlist('gist[contents][][name]')
        new_names = request.POST.getlist('gist[contents][][new_name]')
        values = request.POST.getlist('gist[contents][][value]')
        files = {name: None for name in request.POST['old_names'].split(',')}
        for i,name in enumerate(names):
            files[name] = dict(content = values[i],filename = new_names[i])
        url = 'https://api.github.com/gists/%s' % pk
        headers = {"Authorization": "Bearer %s" % request.user.token}
        data = dict(description = description,files = files)
        r = requests.patch(url,headers=headers,data=json.dumps(data))
        r.raise_for_status()
        data = r.json()
        Gist.objects.filter(pk=pk,owner_id = request.user.id).update(
            description = description,
            files_count = len(new_names),
            files = ','.join(sorted(map(lambda s:s.lower(),new_names))),
            updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ"),
        )
        return redirect(gist.get_absolute_url())
