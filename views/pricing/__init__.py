from base.apps.pricing.models import Plan
from views.base import ListView

class View(ListView):
    context_object_name = "plan_list"
    template_name = "pricing/pricing.html"

    def get_queryset(self, **kwargs):
        return Plan.objects.order_by('name')
