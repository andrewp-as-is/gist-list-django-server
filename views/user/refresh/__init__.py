import time

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from base.apps.github.models import Gist, Token, User, UserRefreshLock, UserRefreshTime

from views.base import View
from views.user.mixins import UserMixin
from utils import get_github_api_data, refresh_user
from .utils import create_github_user, get_github_user, get_lock, get_refresh_time, get_viewer_refresh_count

class View(LoginRequiredMixin, UserMixin, View):
    def get(self,request,*args,**kwargs):
        url = '/'+self.login
        token = Token.objects.get(user_id=request.user.id)
        if token.core_ratelimit_remaining<100:
            return redirect('/token?error=token ratelimit reached')
        refresh_count = get_viewer_refresh_count(self.request.user.id)
        if refresh_count>=10:
            message = '%s users are currently refreshing' % refresh_count
            return redirect('/%s?error=%s' % (self.login,message))
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
