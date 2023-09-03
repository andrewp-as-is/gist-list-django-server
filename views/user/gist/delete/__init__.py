from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

import requests

from base.apps.github.models import Gist, GistDelete, GistStar, Token
from base.apps.github_job.models import UserModificationJob
from views.base import View
from views.user.gist.mixins import GistMixin

"""
https://docs.github.com/en/rest/reference/gists#delete-a-gist
"""

class DeleteView(LoginRequiredMixin,GistMixin,View):
    def get(self, request,*args,**kwargs):
        gist_id = self.gist.id
        user_id = request.user.id
        url = 'https://api.github.com/gists/%s' % gist_id
        token = Token.objects.get(user_id=request.user.id)
        headers = {"Authorization": "Bearer %s" % token.token}
        r = requests.delete(url,headers=headers)
        remaining = r.headers.get('x-ratelimit-remaining',0)
        reset = int(r.headers.get('x-ratelimit-reset',0))
        Token.objects.filter(id=token.id).update(
            core_ratelimit_remaining=remaining,
            core_ratelimit_reset=reset
        )
        url = self.github_user.get_absolute_url()
        if r.status_code in [204]:
            GistStar.objects.filter(gist_id=gist_id).delete()
            Gist.objects.filter(id=gist_id).delete()
            GistDelete.objects.get_or_create(user_id=user_id)
            UserModificationJob.objects.get_or_create(user_id=user_id)
            message = "gist %s was successfully deleted." % gist_id
            return redirect(url+'?message=%s' % message)
        if r.status_code >= 400:
            message = 'ERROR %s: %s' % (r.status_code,r.text)
            return redirect(url+'?error=%s' % message)
