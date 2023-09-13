from base.apps.incident.models import Incident
from views.base import ListView

class View(ListView):
    context_object_name = "incident_list"
    template_name = "status/history/incident_list.html"
    paginate_by = 100

    def get_queryset(self):
        return Incident.objects.order_by('-timestamp')
