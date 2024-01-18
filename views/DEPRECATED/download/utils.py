"""
wget -q https://gist.github.com/<LOGIN>/<ID>/archive/<VERSION>.zip -O <ID>.zip
"""

from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from base.apps.github.models import User
from views.utils import get_gist_model

class View(LoginRequiredMixin,TemplateView):
    template_name = 'download/download.html'

    def get_model(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        return get_gist_model(user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.get_model()
        # todo: version check. list
        context['unknown_version_gist_list'] = list(model.objects.filter(
            owner_id=self.request.user.id,
            version__isnull=True
        ).order_by('id'))
        return context
