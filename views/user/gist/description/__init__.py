from datetime import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

import requests

from base.apps.github.models import Gist
from ..mixins import GistMixin

class View(LoginRequiredMixin,GistMixin,TemplateView):
    template_name = 'user/gist/description/edit.html'

    def post(self, request,*args,**kwargs):
        # todo: check owner
        gist_id = self.gist.id
        url = 'https://api.github.com/gists/%s' % gist_id
        token = Token.objects.get(user_id=request.user.id)
        headers = {"Authorization": "Bearer %s" % token.token}
        description = request.POST.get('description')
        data = json.dumps({'description':description})
        r = requests.patch(url,headers=headers,data=data)
        token.update(r.headers)
        # todo: debug
        Gist.objects.filter(id=gist_id).update(description=description,updated_at=datetime.now())
        return redirect(self.gist.get_absolute_url())
