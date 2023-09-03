from django.views.generic.base import RedirectView, View, TemplateView
from django.views.generic.detail import DetailView
# from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from .mixins import PythonErrorMixin, IncidentMixin

class ListView(PythonErrorMixin,IncidentMixin,ListView):
    pass

class TemplateView(PythonErrorMixin,IncidentMixin, TemplateView):
    pass

class View(PythonErrorMixin, View):
    pass

