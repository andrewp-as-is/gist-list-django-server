from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from base.apps.github.models import GraphqlApiUserFollowersRequest
from views.base import View
from views.user.mixins import UserMixin

# todo: RefreshMixin

class View(LoginRequiredMixin, UserMixin, View):
    def get(self, request, *args, **kwargs):
        priority = 100
        GraphqlApiUserFollowersRequest(
            user_id=self.github_user.id,
            page=1,
            token=self.get_token(),
            priority=priority
        ).save()
        message = "%s followers refresh started" % self.github_user.login
        messages.success(self.request, message)
        return redirect(self.github_user.get_absolute_url()+'/followers')
