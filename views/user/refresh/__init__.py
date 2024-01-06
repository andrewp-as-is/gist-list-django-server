import time

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from base.apps.github.models import Gist, Token, User, UserRefresh

from views.base import View
from views.user.mixins import UserMixin
from utils import get_github_api_data, refresh_user
from .utils import (
    create_github_user,
    get_github_user,
    get_lock,
    get_viewer_refresh_count,
)


class View(LoginRequiredMixin, UserMixin, View):
    def get(self, request, *args, **kwargs):
        url = "/" + self.login
        token = Token.objects.get(user_id=request.user.id)
        if token.core_ratelimit_remaining < 100:
            messages.success(self.request, "token ratelimit reached")
            return redirect(url)
        refresh_count = get_viewer_refresh_count(self.request.user.id)
        if refresh_count >= 10:
            message = "%s users are currently refreshing" % refresh_count
            messages.warning(self.request, message)
            return redirect(url)
        if self.github_user:
            if get_lock(self.github_user.id):
                message = "%s already refreshing" % self.login
                messages.warning(self.request, message)
                return redirect(url)
            if self.github_user.id == self.request.user.id:  # authenticated user
                refresh_user(self.request,self.github_user, priority=100)
            else:  # other user
                refresh_user(self.request,self.github_user, priority=50)
            message = "refresh started"
            messages.success(self.request, message)
            return redirect(url)
        else:  # unknown user
            url = "https://api.github.com/users/%s" % self.login
            data = get_github_api_data(url, token.token)
            if data:
                user = create_github_user(data)
                message = "refresh started"
                messages.success(self.request, message)
                return redirect(url)
            else:  # 404
                defaults = dict(timestamp=int(time.time()))
                User404.objects.update_or_create(defaults, login=self.login)
                message = "User Not Found"
                messages.warning(self.request, message)
                return redirect(url)
