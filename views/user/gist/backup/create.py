import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from base.apps.github.models import Gist
from base.apps.http_client.models import RequestJob
from views.base import View
from ..mixins import GistMixin

class View(LoginRequiredMixin,GistMixin,View):
    def get(self, request,*args,**kwargs):
        gist_id = self.gist.id
        user_id = request.user.id
        # todo: RequestJob
