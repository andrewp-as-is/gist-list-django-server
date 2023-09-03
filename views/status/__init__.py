from datetime import datetime
import time

from django.views.generic.base import TemplateView

from base.apps.healthcheck.models import Healthcheck
from base.apps.incident.models import Incident

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
        check_list = list(Healthcheck.objects.all().order_by('name'))
        if check_list:
            check_timestamp = max(map(lambda c:c.timestamp,check_list))
            if check_timestamp+60>int(time.time()):
                context['check_list'] = check_list
                context['incident_list'] = list(Incident.objects.order_by('-timestamp')[0:100])
        return context
