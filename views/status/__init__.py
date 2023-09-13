from datetime import datetime
import time

from django.views.generic.base import TemplateView

from base.apps.healthcheck.models import Healthcheck
from base.apps.http_request_job.models import Job as HttpRequestJob
from base.apps.incident.models import Incident
from base.apps.github_user_refresh.models import Lock

class View(TemplateView):
    template_name = "status/status.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        success = True
        for check in context.get('check_list',[]):
            if check.success:
                success = False
        status = 200 if success else 500
        return self.render_to_response(context, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['healthcheck_success'] = Healthcheck.objects.filter(success=False).count()==0
        context['http_request_count'] = HttpRequestJob.objects.all().count()
        context['incident_count'] = Incident.objects.all().count()
        context['github_user_refresh_count'] = Lock.objects.all().count()
        return context
