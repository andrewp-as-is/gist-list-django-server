from datetime import datetime
import time

from base.apps.status.models import Status
from views.base import TemplateView

class View(TemplateView):
    template_name = "status/status.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #success = True
        #for check in context.get('check_list',[]):
        #    if check.success:
        #        success = False
        #status = 200 if success else 500
        status = 200
        return self.render_to_response(context, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = Status.objects.all().first()
        return context
