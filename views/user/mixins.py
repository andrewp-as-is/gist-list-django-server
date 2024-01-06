from datetime import datetime, timedelta


from django.db.models import Count, F
from django.shortcuts import redirect, render
import requests

from base.apps.github.models import (
    Gist,
    User,
    User404,
)
from base.apps.github_live_matview.models import UserStatus
from base.apps.github_live_matview.utils import get_model as get_live_matview_model
from base.apps.github_matview.utils import get_model as get_matview_model
from base.apps.user.models import GithubUserRefresh, GithubUserRefreshLock

def get_model(tablename,live_matview_list):
    if tablename in live_matview_list:
        return get_live_matview_model(tablename)
    return get_matview_model(tablename)


class UserMixin:
    def dispatch(self, *args, **kwargs):
        self.login = self.kwargs["login"]
        # /ID -> /LOGIN/ID redirect
        try:
            gist = Gist.objects.get(id=self.login)
            return redirect(gist.get_absolute_url())
        except Gist.DoesNotExist:
            pass
        try:
            self.github_user = User.objects.get(login=self.kwargs["login"])
            self.github_user_id = self.github_user.id
            authenticated = self.request.user.id == self.github_user.id
            try:
                user_status = UserStatus.objects.get(user_id=self.github_user.id)
                live_matview_list = user_status.matview_list
            except UserStatus.DoesNotExist:
                live_matview_list = []
            try:
                self.github_user_refresh = GithubUserRefresh.objects.get(
                    user_id=self.github_user.id
                )
            except GithubUserRefresh.DoesNotExist:
                self.github_user_refresh = None
        except User.DoesNotExist:
            self.github_user = None
            self.github_user_id = None
        self.gist_model = get_model('gist',live_matview_list)
        self.follower_model = get_model('follower',live_matview_list)
        self.following_model = get_model('following',live_matview_list)
        self.gist_language_model = get_model('gist_language',live_matview_list)
        self.gist_star_model = get_model('gist_star',live_matview_list)
        self.gist_tag_model = get_model('gist_tag',live_matview_list)
        self.user_model = get_model('user',live_matview_list)
        response = super().dispatch(*args, **kwargs)
        #if response.status_code in [200, 304] and self.refreshed_at:
       #     response["ETag"] = self.refreshed_at
        #    response["Last-Modified"] = self.refreshed_at
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login"] = self.login
        if hasattr(self, "github_user") and self.github_user:
            context["github_user"] = self.github_user
            qs = self.gist_model.objects.filter(owner_id=self.github_user.id)
            if (
                not self.request.user.is_authenticated
                or self.github_user.id != self.request.user.id
            ):
                qs = qs.filter(public=True)
            context["gists_count"] = qs.count()
            context["forks_count"] = qs.filter(fork=True).count()
            context["github_user_refresh"] = self.github_user_refresh
        else:
            try:
                context["user404"] = User404.objects.get(login=self.login)
            except User404.DoesNotExist:
                pass
        context.update(login=self.login)
        return context
