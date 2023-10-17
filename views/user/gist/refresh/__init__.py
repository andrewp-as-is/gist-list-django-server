import time

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from base.apps.github.models import Gist, Token, GistRefreshLock #, UserRefreshTime

from views.base import View
from views.user.gist.mixins import GistMixin
from utils import refresh_gist

class View(LoginRequiredMixin, GistMixin, View):
    def get(self,request,*args,**kwargs):
        url = self.gist.get_absolute_url()
        token = Token.objects.get(user_id=request.user.id)
        if token.core_ratelimit_remaining<100:
            messages.success(self.request, 'token ratelimit reached')
            return redirect(url)
        refresh_gist(self.gist,token,priority=100)
        message = 'refresh started'
        messages.success(self.request, message)
        return redirect(url)
