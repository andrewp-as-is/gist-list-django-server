#!/usr/bin/env python
from datetime import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

import requests

from base.apps.github.models import Gist
from django.views.generic.base import TemplateView

class GistCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'gist/gist_create.html'

    def post(self, request):
        description = request.POST.get('gist[description]')
        filename = request.POST.get('gist[filename]')
        code = request.POST.get('gist[code]')
        public = request.POST.get('gist[public]') == '1'
        headers = {"Authorization": "Bearer %s" % request.user.token}
        data = dict(
            description = description,
            public = public,
            files = {filename: {'content':code}}
        )
        r = requests.post('https://api.github.com/gists',headers=headers,data=json.dumps(data))
        r.raise_for_status()
        data = r.json()
        gist = Gist(
            id = data['id'],
            owner_id = request.user.id,
            public = public,
            description = description,
            created_at = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
            updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ"),
            files_count = 1,
            files = filename
        )
        gist.save()
        return redirect(gist.get_absolute_url())
