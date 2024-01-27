import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from base.apps.github.models import Gist
from base.apps.http_client.models import RequestJob
from views.base import TemplateView
from ..mixins import GistMixin

class View(LoginRequiredMixin,GistMixin,TemplateView):
    template_name = 'user/gist/backup/backup.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
