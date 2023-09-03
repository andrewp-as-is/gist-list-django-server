#!/usr/bin/env python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import requests

from base.apps.github.models import GistStar
from views.base import View as _View

class GistUnstarView(LoginRequiredMixin,_View):
    def get(self, request,pk):
        headers = {"Authorization": "Bearer %s" % request.user.token}
        r = requests.delete('https://api.github.com/gists/%s/star' % pk,headers=headers)
        r.raise_for_status()
        GistStar.objects.filter(gist_id=pk,owner_id=request.user.id).delete()
        return self.next()
