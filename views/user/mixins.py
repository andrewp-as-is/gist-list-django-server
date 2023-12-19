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
from base.apps.github_modification_matview.models import MatviewTime
from utils import (
    get_gist_model,
    get_gist_language_model,
    get_gist_tag_model,
    get_user_model,
)


class UserMixin:
    def dispatch(self, *args, **kwargs):
        self.login = self.kwargs["login"]
        # /ID -> /LOGIN/ID redirect
        self.refreshed_at = None
        self.modification_matview_time = None
        try:
            gist = Gist.objects.get(id=self.login)
            return redirect(gist.get_absolute_url())
        except Gist.DoesNotExist:
            pass
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
            try:
                self.modification_matview_time = MatviewTime.objects.get(
                    user_id=self.github_user.id
                )
            except MatviewTime.DoesNotExist:
                pass
        except User.DoesNotExist:
            self.github_user = None
            self.github_user_id = None
        self.gist_model = get_gist_model(self.modification_matview_time)
        self.gist_language_model = get_gist_language_model(
            self.modification_matview_time
        )
        self.gist_tag_model = get_gist_tag_model(self.modification_matview_time)
        # self.user_model = get_user_model(self.modification_matview_time)
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
