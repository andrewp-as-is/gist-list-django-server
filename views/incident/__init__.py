from base.apps.incident.models import Incident
from views.base import ListView

class View(ListView):
    context_object_name = "incident_list"
    template_name = "incident/incident_list.html"

    def get_queryset(self, **kwargs):
        return Incident.objects.order_by('-timestamp')
