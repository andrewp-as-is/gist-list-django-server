from django.views.generic.base import TemplateView

from base.apps.http_request_job.models import Job
from views.user.mixins import UserMixin
from .utils import get_user_id

class View(UserMixin, TemplateView):
    template_name = 'user/refresh_status/status.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.github_user:
            queryset = Job.objects.filter(
                url__contains='https://api.github.com/user/%s' % self.github_user.id
            ).order_by('url')
            job_list = list(filter(
                lambda j:get_user_id(j.url)==self.github_user.id,
                queryset
            ))
            context['job_list'] = job_list
        return context
