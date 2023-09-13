from base.apps.healthcheck.models import Healthcheck
from views.base import ListView

class View(ListView):
    context_object_name = "healthcheck_list"
    template_name = "healthcheck/healthcheck_list.html"

    def get_queryset(self, **kwargs):
        return Healthcheck.objects.order_by('name')
