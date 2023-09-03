from django.shortcuts import render

from base.apps.error.models import PythonError
from base.apps.error.utils import save_python_error
from base.apps.incident.models import Incident


class PythonErrorMixin:
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            save_python_error(e)
            response = render(self.request,'500.html', status=500)
            return response

class IncidentMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incident_list'] = list(Incident.objects.order_by('-timestamp')[0:10])
        return context
