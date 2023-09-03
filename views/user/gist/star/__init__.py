from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Max, Value
from django.db.models.functions import Coalesce
from django.shortcuts import redirect

import requests

from base.apps.github.models import GistStar
from views.base import View as _View
from views.user.gist.mixins import GistMixin

from ..utils import update_user_stars

"""
https://docs.github.com/en/rest/reference/gists#star-a-gist
required scope: star_gist (undocumented)
"""

class StarView(LoginRequiredMixin,GistMixin,_View):
    def get(self, request,*args,**kwargs):
        gist_id = self.kwargs['pk']
        user_id = self.request.user.id
        token = Token.objects.get(user_id=user_id)
        headers = {
            "Authorization": "Bearer %s" % token.token,
            "Accept": "application/vnd.github.v3+json"
        }
        url = 'https://api.github.com/gists/%s/star' % gist_id
        r = requests.put(url,headers=headers)
        token.update(r.headers)
        if r.status_code in [204]:
            max_order = GistStar.objects.filter(user_id=user_id).aggregate(
                max_order=Coalesce(Max('starred_order'), Value(0))
            )['max_order']
            starred_order = max_order+1
            GistStar.objects.get_or_create(gist_id=gist_id,user_id=user_id,starred_order=starred_order)
            stargazers_count = GistStar.objects.filter(gist_id=gist_id).count()
            Gist.objects.filter(id=gist_id).update(stargazers_count=stargazers_count)
            update_user_stars(user_id)
        url = self.gist.get_absolute_url()
        return redirect(url)

"""
if self.gist.stargazers_count is not None:
    Gist.objects.filter(id=gist_id).update(stargazers_count=F('stargazers_count')+1)
else:
    Gist.objects.filter(id=gist_id).update(stargazers_count=1)
"""
