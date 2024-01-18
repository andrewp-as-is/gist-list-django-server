"""
https://docs.github.com/en/rest/reference/gists#unstar-a-gist
required scope: star_gist (undocumented)
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import redirect

import requests

from base.apps.github.models import Gist
from views.user.gist.mixins import GistMixin
from views.base import View as _View

from ..utils import update_user_stars



class View(LoginRequiredMixin,GistMixin,_View):
    def get(self, request,*args,**kwargs):
        gist_id = self.kwargs['pk']
        user_id = self.request.user.id
        token = Token.objects.get(user_id=user_id)
        headers = {"Authorization": "Bearer %s" % token.token}
        url = 'https://api.github.com/gists/%s/star' % gist_id
        r = requests.delete(url,headers=headers)
        token.update(r.headers)
        if r.status_code in [204]:
            GistStar.objects.filter(gist_id=gist_id,user_id=user_id).delete()
            Gist.objects.filter(id=gist_id).update(stargazers_count=F('stargazers_count')-1)
            update_user_stars(user_id)
        url = self.gist.get_absolute_url()
        return redirect(url)
