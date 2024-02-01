from django.views.generic.base import RedirectView, View, TemplateView
from django.views.generic.detail import DetailView

# from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from .mixins import Mixin #, PythonErrorMixin
# from django_error.mixins import ViewErrorMixin

PAGINATE_BY_LIST = [10,20,50,100,1000]
PAGINATE_BY_DEFAULT = 50
PAGINATE_BY_KEY= 'v'

# class ListView(ViewErrorMixin, ListView):
class ListView(Mixin,ListView):
    paginate_by = None

    def get_paginate_by(self, request):
        if self.paginate_by:  # hardcoded
            return self.paginate_by
        value = self.request.GET.get(PAGINATE_BY_KEY, "")
        if value.isdigit() and int(value) in PAGINATE_BY_LIST:
            return int(value)
        return PAGINATE_BY_DEFAULT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        details = context_data.get('details',{})
        details['view'] = dict(menu_item_list = self.get_details_view_menu_item_list())
        context_data['details'] = details
        context['context_data'] = context_data
        return context

    def get_details_view_menu_item_list(self):
        menu_item_list = []
        value = self.request.GET.get(PAGINATE_BY_KEY,'')
        default_value = PAGINATE_BY_DEFAULT
        for count in PAGINATE_BY_LIST:
            menu_item_list+=[dict(
                description=count,
                selected=value==str(count) or (not value and count==default_value),
                url=self.get_url(v=str(count))
            )]
        return menu_item_list


class TemplateView(Mixin,TemplateView):
    pass


class View(Mixin,View):
    pass
