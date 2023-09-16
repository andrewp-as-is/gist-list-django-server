from datetime import datetime, timedelta


from django.db.models import Count, F
from django.shortcuts import redirect, render
import requests

from base.apps.github.models import Gist, User, User404, UserRefreshLock, UserRefreshTime

class UserMixin:
    def dispatch(self, *args, **kwargs):
        self.login = self.kwargs['login']
        # /ID -> /LOGIN/ID redirect
        self.refresh_time = None
        try:
            gist = Gist.objects.get(id=self.login)
            return redirect(gist.get_absolute_url())
        except Gist.DoesNotExist:
            pass
        try:
            User.objects.get(login=self.login)
            self.github_user = User.objects.get(login=self.kwargs['login'])
            self.github_user_id = self.github_user.id
            authenticated = (self.request.user.id == self.github_user.id)
            try:
                self.refresh_lock = UserRefreshLock.objects.get(user_id=self.github_user.id)
            except UserRefreshLock.DoesNotExist:
                self.refresh_lock = None
            try:
                self.refresh_time = UserRefreshTime.objects.get(
                    user_id=self.github_user.id,
                    authenticated=authenticated
                )
            except UserRefreshTime.DoesNotExist:
                pass
        except User.DoesNotExist:
            self.github_user = None
            self.github_user_id = None
        response = super().dispatch(*args, **kwargs)
        if response.status_code in [200,304] and self.refresh_time:
            response['ETag'] = self.refresh_time.timestamp
            response['Last-Modified'] = self.refresh_time.timestamp
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login'] = self.login
        is_syncing = False
        is_owner = False
        if hasattr(self,'github_user') and self.github_user:
            context['github_user'] = self.github_user
            is_owner = self.request.user.is_authenticated and self.request.user.login == self.github_user.login
            gists_count = self.github_user.public_gists_count or 0
            forks_count = self.github_user.public_forks_count or 0
            if self.request.user.is_authenticated and self.github_user.id == self.request.user.id:
                gists_count+=(self.github_user.private_gists_count or 0)
                forks_count+=(self.github_user.private_forks_count or 0)
            context['gists_count'] = gists_count
            context['forks_count'] = forks_count
            context['refresh_lock'] = self.refresh_lock
            context['refresh_time'] = self.refresh_time
        else:
            try:
                context['user404'] = User404.objects.get(login=self.login)
            except User404.DoesNotExist:
                pass
        context.update(
            login = self.login,
            is_owner = is_owner
        )
        return context

