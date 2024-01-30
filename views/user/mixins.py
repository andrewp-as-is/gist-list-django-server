from datetime import datetime, timedelta


from django.conf import settings
from django.db.models import Count, F
from django.shortcuts import redirect, render
import requests

from base.apps.github.models import (
    Gist,
    User,
    UserStat,
    UserTableModification,
    User404,
)
from base.apps.github_default_matview.models import User as DefaultUser
from base.apps.github_default_matview.utils import get_model as get_matview_model
from base.apps.github_recent_matview.models import User as RecentUser
from base.apps.github_recent_matview.utils import get_model as get_live_matview_model
from base.apps.postgres.models import Matview
from base.apps.user.models import GithubUserRefresh, GithubUserRefreshLock

def get_model(tablename,live_matview_list):
    if tablename in live_matview_list:
        return get_live_matview_model(tablename)
    return get_matview_model(tablename)


class UserMixin:
    def dispatch(self, *args, **kwargs):
        self.login = self.kwargs["login"]
        # /ID -> /LOGIN/ID redirect
        # todo: gist ID length check/validate
        # todo2: first github gist IDs (first users? /users?page=1)
        try:
            gist = Gist.objects.get(id=self.login)
            return redirect(gist.get_absolute_url())
        except Gist.DoesNotExist:
            pass
        live_matview_list = []
        self.github_user_refresh_lock = None
        self.github_user_stat = None
        try:
            self.github_user = User.objects.get(login=self.kwargs["login"])
            authenticated = self.request.user.id == self.github_user.id
            user_id = self.github_user.id
            try:
                self.github_user_stat = UserStat.objects.get(user_id=user_id)
            except UserStat.DoesNotExist:
                pass
            try:
                self.github_user_refresh_lock = GithubUserRefreshLock.objects.get(github_user_id=user_id)
            except GithubUserRefreshLock.DoesNotExist:
                pass
        except User.DoesNotExist:
            self.github_user = None
        response = super().dispatch(*args, **kwargs)
        #if response.status_code in [200, 304] and self.refreshed_at:
       #     response["ETag"] = self.refreshed_at
        #    response["Last-Modified"] = self.refreshed_at
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        context_data["login"] = self.login
        if hasattr(self, "github_user") and self.github_user:
            languages_count, tags_count = None, None
            if self.github_user_stat:
                languages_count = 42
                tags_count = 42
                #languages_count=len(self.github_user_stat.public_language_stat.splitlines())
                #tags_count=len(self.github_user_stat.public_tag_stat.splitlines())
            context_data["github_user"] = self.github_user
            context_data["github_user_stat"] = self.github_user_stat
            context_data["github_user_refresh_lock"] = self.github_user_refresh_lock
            if self.github_user_stat:
                gists_count = self.github_user_stat.public_gists_count
                forks_count = self.github_user_stat.public_forks_count
                if self.github_user.id==self.request.user.id:
                    if gists_count:
                        gists_count+=self.github_user_stat.secret_gists_count or 0
                    if forks_count:
                        forks_count+=self.github_user_stat.secret_forks_count or 0
                links = context_data.get('links',{})
                links.update(
                    forked=dict(
                        count=forks_count,
                        selected = self.request.path.endswith('/forked')
                    ),
                    starred=dict(
                        count=self.github_user_stat.stars_count,
                        selected = self.request.path.endswith('/starred')
                    ),
                    trash=dict(
                        count=self.github_user_stat.trash_count,
                        selected = self.request.path.endswith('/trash')
                    )
                )
                links['gists'] = dict(
                    count=gists_count,
                    selected=not bool(any(filter(lambda d:d['selected'],links.values())))
                )
                context_data["links"] = links
        else:
            try:
                context_data["user404"] = User404.objects.get(login=self.login)
            except User404.DoesNotExist:
                pass
        context_data.update(login=self.login)
        context['context_data'] = context_data
        return context
