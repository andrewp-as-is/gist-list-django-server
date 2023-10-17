from django.views.generic.base import RedirectView, View, TemplateView
from django.views.generic.detail import DetailView

# from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from . import details

# from .mixins import PythonErrorMixin
# from django_error.mixins import ViewErrorMixin


# class ListView(ViewErrorMixin, ListView):
class ListView(ListView):
    paginate_by = None

    def get_paginate_by(self, request):
        if self.paginate_by:  # hardcoded
            return self.paginate_by
        value = self.request.GET.get("v", "")
        view_details = details.View(self.request)
        values = list(map(lambda i: i["value"], view_details.get_menu_item_list()))
        if value and value.isdigit() and value in values:
            return int(value)
        return view_details.get_default_value()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_details"] = details.View(self.request)
        return context


class TemplateView(TemplateView):
    pass


class View(View):
    pass
