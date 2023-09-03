import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

import requests

from base.apps.github.models import Gist
from base.apps.github.models import Token

"""
https://docs.github.com/en/rest/reference/gists#create-a-gist
"""

class View(LoginRequiredMixin,TemplateView):
    template_name = 'new/new.html'

    def post(self, request,*args,**kwargs):
        token = Token.objects.get(user_id=self.request.user.id)
        public = request.POST.get('gist[public]') == '1'
        description = request.POST.get('gist[description]')
        names = request.POST.getlist('gist[contents][][name]')
        values = request.POST.getlist('gist[contents][][value]')
        files = {}
        for i,name in enumerate(names):
            files[name] = dict(content = values[i],filename = names[i])
        url = 'https://api.github.com/gists'
        headers = {"Authorization": "Bearer %s" % token.token}
        data = dict(public=public,description = description,files = files)
        r = requests.post(url,headers=headers,data=json.dumps(data))
        # token.update(r.headers)
        # r.raise_for_status()
        if r.status_code in [201]:
            data = r.json()
            # todo
            Gist(id = data['id'],owner_id = data['owner']['id'],**get_kwargs(data)).save()
            #
        return redirect('/')
