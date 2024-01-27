from datetime import datetime, timedelta


from django.conf import settings
from django.db.models import Count, F
from django.shortcuts import redirect, render
import requests

from base.apps.github.models import (
    Gist,
    User,
    UserRefresh,
    UserTableModification,
    User404,
)
from base.apps.github_live_matview.utils import get_model as get_live_matview_model
from base.apps.github_default_matview.utils import get_model as get_matview_model
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
        try:
            gist = Gist.objects.get(id=self.login)
            return redirect(gist.get_absolute_url())
        except Gist.DoesNotExist:
            pass
        live_matview_list = []
        self.github_user_refresh = None
        self.github_user_refresh_lock = None
        self.github_user_stat = None
        try:
            self.github_user = User.objects.get(login=self.kwargs["login"])
            authenticated = self.request.user.id == self.github_user.id
            matview_list = list(Matview.objects.filter(
                schemaname='github_live_matview'
            ).all())
            table_list = list(UserTableModification.objects.filter(user_id=self.github_user.id))
            matviewname2timestamp = {m.matviewname:m.refreshed_at for m in matview_list}
            tablename2timestamp = {t.tablename:t.modified_at for t in table_list}
            for matviewname,refreshed_at in matviewname2timestamp.items():
                modified_at = tablename2timestamp.get(matviewname,None)
                if modified_at and refreshed_at>modified_at:
                    live_matview_list+=[matviewname]
            try:
                self.github_user_refresh = UserRefresh.objects.get(user_id=self.github_user.id)
            except UserRefresh.DoesNotExist:
                pass
            try:
                self.github_user_refresh_lock = GithubUserRefreshLock.objects.get(github_user_id=self.github_user.id)
            except GithubUserRefreshLock.DoesNotExist:
                pass
        except User.DoesNotExist:
            self.github_user = None

        self.follower_model = get_model('follower',live_matview_list)
        self.following_model = get_model('following',live_matview_list)
        self.gist_model = get_model('gist',live_matview_list)
        self.gist_language_model = get_model('gist_language',live_matview_list)
        self.gist_star_model = get_model('gist_star',live_matview_list)
        self.gist_tag_model = get_model('gist_tag',live_matview_list)
        self.starred_gist_model = get_model('starred_gist',live_matview_list)
        self.user_model = get_model('user',live_matview_list)
        self.user_stat_model = get_model('user_stat',live_matview_list)
        if settings.DEBUG:
            print('github_live_matview (%s): %s' % (len(live_matview_list),','.join(live_matview_list)))
        try:
            if self.github_user:
                self.github_user_stat = self.user_stat_model.objects.get(user_id=self.github_user.id)
        except self.user_stat_model.DoesNotExist:
            pass
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
            context["github_user_refresh"] = self.github_user_refresh
            context["github_user_refresh_lock"] = self.github_user_refresh_lock
            qs = self.gist_model.objects.filter(owner_id=self.github_user.id)
            if (
                not self.request.user.is_authenticated
                or self.github_user.id != self.request.user.id
            ):
                qs = qs.filter(public=True)
            if self.github_user_stat:
                gists_count = self.github_user_stat.public_gists_count
                forks_count = self.github_user_stat.public_forks_count
                if self.github_user.id==self.request.user.id:
                    if gists_count:
                        gists_count+=self.github_user_stat.secret_gists_count or 0
                    if forks_count:
                        forks_count+=self.github_user_stat.secret_forks_count or 0
                context["github_user_stat"] = dict(
                    gists_count=gists_count,
                    forks_count=forks_count,
                    stars_count=self.github_user_stat.stars_count,
                    languages_count=len(self.github_user_stat.language_list),
                    tags_count=len(self.github_user_stat.tag_list),
                )
        else:
            try:
                context["user404"] = User404.objects.get(login=self.login)
            except User404.DoesNotExist:
                pass
        context.update(login=self.login)
        return context
