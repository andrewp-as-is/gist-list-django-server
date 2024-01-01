from datetime import datetime, timedelta


from django.db.models import Count, F
from django.shortcuts import redirect, render
import requests

from base.apps.github.models import (
    Gist,
    User,
    User404,
    UserLock,
)
from base.apps.github_live_matview.models import UserStatus
from base.apps.github_live_matview.utils import get_model as get_live_matview_model
from base.apps.github_matview.utils import get_model as get_matview_model

def get_model(tablename,live_matview_list):
    if tablename in live_matview_list:
        return get_live_matview_model(tablename)
    return get_matview_model(tablename)


class UserMixin:
    def dispatch(self, *args, **kwargs):
        self.login = self.kwargs["login"]
        # /ID -> /LOGIN/ID redirect
        self.refreshed_at = None
        self.user_meta = None
        try:
            gist = Gist.objects.get(id=self.login)
            return redirect(gist.get_absolute_url())
        except Gist.DoesNotExist:
            pass
        try:
            user_status = UserStatus.objects.get(user_id=)
            self.live_matview_list = user_status.matview_list
        except UserStatus.DoesNotExist:
            self.live_matview_list = []
        try:
            User.objects.get(login=self.login)
            self.github_user = User.objects.get(login=self.kwargs["login"])
            self.github_user_id = self.github_user.id
            authenticated = self.request.user.id == self.github_user.id
            self.refreshed_at = self.github_user.refreshed_at
            if authenticated:
                self.refreshed_at = self.github_user.secret_refreshed_at
            try:
                self.refresh_lock = UserLock.objects.get(
                    user_id=self.github_user.id
                )
            except UserLock.DoesNotExist:
                self.refresh_lock = None
        except User.DoesNotExist:
            self.github_user = None
            self.github_user_id = None
        self.follower_model = get_model('follower')
        self.following_model = get_model('following')
        self.gist_model = get_model('gist')
        self.gist_language_model = get_model('gist_language')
        self.gist_star_model = get_model('gist_star')
        self.gist_tag_model = get_model('gist_tag')
        self.user_model = get_model('user')
        response = super().dispatch(*args, **kwargs)
        if response.status_code in [200, 304] and self.refreshed_at:
            response["ETag"] = self.refreshed_at
            response["Last-Modified"] = self.refreshed_at
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
            context["refresh_lock"] = self.refresh_lock
        else:
            try:
                context["user404"] = User404.objects.get(login=self.login)
            except User404.DoesNotExist:
                pass
        context.update(login=self.login)
        return context
