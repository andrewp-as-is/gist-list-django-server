import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect

import requests

from base.apps.github.models import Gist, GistStar, Token, Trash, UserStat
from views.base import View
from ..mixins import GistMixin

"""
https://docs.github.com/en/rest/reference/gists#delete-a-gist
"""

class View(LoginRequiredMixin,GistMixin,View):
    def get(self, request,*args,**kwargs):
        gist_id = self.gist.id
        user_id = request.user.id
        url = 'https://api.github.com/gists/%s' % gist_id
        token = Token.objects.get(user_id=request.user.id)
        headers = {"Authorization": "Bearer %s" % token.token}
        # github.trash
        defaults = dict(
            owner_id=self.gist.owner_id,
            fork_of_id=self.gist.fork_of_id,
            public=self.gist.public,
            description=self.gist.description,
            filename_list=self.gist.filename_list,
            file_size_list=self.gist.file_size_list,
            language_list=self.gist.language_list,
            deleted_at = int(time.time())
        )
        Trash.objects.get_or_create(defaults,gist_id=gist_id)
        r = requests.delete(url,headers=headers)
        remaining = r.headers.get('x-ratelimit-remaining',0)
        reset = int(r.headers.get('x-ratelimit-reset',0))
        Token.objects.filter(id=token.id).update(
            core_ratelimit_remaining=remaining,
            core_ratelimit_reset_at=reset
        )
        url = self.github_user.get_absolute_url()
        if r.status_code >= 400:
            return HttpResponse(r.text, status=r.status_code)
        if r.status_code in [204]: # DELETED
            Gist.objects.filter(id=gist_id).delete()
            trash_count = Trash.objects.filter(owner_id=user_id).count()
            UserStat.objects.filter(user_id=user_id).update(
                gist_modified_at=int(time.time()),
                trash_count=trash_count,
            )
            return redirect(self.github_user.get_absolute_url())
