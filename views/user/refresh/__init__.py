import time

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from base.apps.github.models import GraphqlApiUserGistsRequest, GraphqlApiViewerGistsRequest, Gist, RestApiAuthenticatedUserGistsRequest, RestApiUserGistsRequest, Token, User, UserMapping

from views.base import View
from views.user.mixins import UserMixin
from utils import get_github_api_data, refresh_user
from .utils import (
    create_github_user,
    get_github_user,
)


class View(LoginRequiredMixin, UserMixin, View):
    def get(self, request, *args, **kwargs):
        priority = 100
        if self.github_user:
            # todo: rest, graphql, public vs auth, etc
            RestApiUserGistsRequest(
                user_id=self.github_user.id,
                page=1,
                token=self.get_token(),
                priority=priority
            ).save()
            message = "%s gists refresh started" % self.github_user.login
            messages.success(self.request, message)
            return redirect(self.github_user.get_absolute_url())
        else:
            url = "/" + self.login
            token = Token.objects.get(user_id=request.user.id)
            if token.core_ratelimit_remaining < 100:
                messages.success(self.request, "token ratelimit reached")
                return redirect(url)
            print("LOCK REMOVED")
            locks_count= 0
            # locks_count = get_locks_count(self.request.user.id)
            if locks_count >= 10:
                message = "%s users are currently refreshing" % locks_count
                messages.warning(self.request, message)
                return redirect(url)
            print('self.github_user: %s' % self.github_user)
            if self.github_user:
                print('TODO: LOCK CHECK')
                #if get_github_user_lock(self.github_user.id):
               #     message = "%s already refreshing" % self.login
               ##     messages.warning(self.request, message)
                #    return redirect(url)
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
                    defaults = dict(created_at=int(time.time()))
                    UserMapping.objects.update_or_create(defaults, login=self.login,user_id=None)
                    message = "User Not Found"
                    messages.warning(self.request, message)
                    return redirect(url)
