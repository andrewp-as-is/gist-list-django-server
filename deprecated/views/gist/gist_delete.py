#!/usr/bin/env python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import requests

from base.apps.github.models import Gist
from views.base import View as _View

class GistTrashView(LoginRequiredMixin,_View):
    def get(self, request,pk):
        headers = {"Authorization": "Bearer %s" % request.user.token}
        r = requests.delete('https://api.github.com/gists/%s' % pk,headers=headers)
        print(r.text)
        r.raise_for_status()
        Gist.objects.filter(pk=pk,owner_id=request.user.id).delete()
        return redirect('/%s/' % request.user.login)
