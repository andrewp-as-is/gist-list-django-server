import time

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from base.apps.github.models import User, Token
from base.apps.github_user_refresh.models import Lock, Time, User404

from views.base import View
from views.user.mixins import UserMixin
from utils import get_github_api_data, refresh_user
from .utils import create_github_user, get_github_user, get_lock, get_refresh_time, get_token_lock

class View(LoginRequiredMixin, UserMixin, View):
    def get(self,request,*args,**kwargs):
        url = '/'+self.login
        token = Token.objects.get(user_id=request.user.id)
        if token.core_ratelimit_remaining<100:
            return redirect('/token?error=token ratelimit reached')
        lock = get_token_lock(token.id)
        if lock:
            github_user = get_github_user(lock.user_id)
            if github_user:
                message = '%s refresh running' % github_user.login
                return redirect('/%s?error=%s' % (self.login,message))
        get_token_lock
        if self.github_user:
            if get_lock(self.github_user.id):
                return redirect('/%s?error=already refreshing' % self.login)
            if self.github_user.id==self.request.user.id: # authenticated user
                refresh_user(self.github_user,token,priority=100)
            else: # other user
                # self.refresh_time
                # refresh_time = get_refresh_time(self.github_user.id)
                # if not refresh_time or refresh_time.timestamp+60*60<int(time.time()):
                refresh_user(self.github_user,token,priority=50)
            return redirect('/'+self.login)
        else: # unknown user
            url = 'https://api.github.com/users/%s' % self.login
            data = get_github_api_data(url,token.token)
            if data:
                user = create_github_user(data)
                refresh_user(user,token,priority=90)
                return redirect('/%s?message=refresh started' % self.login)
            else: # 404
                defaults = dict(timestamp=int(time.time()))
                User404.objects.update_or_create(defaults,login=self.login)
                return redirect('/%s?error=User Not Found' % self.login)
