from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from base.apps.github.models import Gist, GistStar, Trash, UserStat

from views.base import View
from views.user.mixins import UserMixin

class View(LoginRequiredMixin, UserMixin, View):
    def get(self, request, *args, **kwargs):
        url = request.GET.get('next',"/" + self.login)
        user_id = request.user.id
        public_gists_count=Gist.objects.filter(owner_id=user_id,public=True).count()
        secret_gists_count=Gist.objects.filter(owner_id=user_id,public=False).count()
        trash_count=Trash.objects.filter(owner_id=user_id).count()
        UserStat.objects.filter(user_id=user_id).update(
            public_gists_count=public_gists_count,
            secret_gists_count=secret_gists_count,
            trash_count=trash_count
        )
        return redirect(url)
