from base.apps.github.models import Gist, GistFile
from views.base import ListView
from ..mixins import UserMixin

SORT_ITEM_LIST = [
    {'value':'name','description':'Name'},
    {'value':'size','description':'Size'},
    {'value':'type','description':'Type'},
    {'value':'gist','description':'Gist'},
]

class View(UserMixin,ListView):
    context_object_name = "gist_file_list"
    template_name = "user/files/gist_file_list.html"
    default_order_by_list = ['row_number_over_name']

    def get_model(self):
        return GistFile

    def get_queryset(self,**kwargs):
        model = self.get_model()
        qs = model.objects.filter(owner_id=self.github_user.id)
        q = self.request.GET.get('q','').strip()
        file_type = self.request.GET.get('type','').strip()
        if q:
            qs = qs.filter(name__icontains=q)
        if file_type:
            print('file_type: %s' % file_type)
            qs = qs.filter(type=file_type)
        qs = qs.select_related()
        order_by_list = self.get_queryset_order_by_list()
        print('order_by_list: %s' % order_by_list)
        return qs.order_by(*order_by_list)

    def get_queryset_order_by_list(self, **kwargs):
        model = self.get_model()
        sort = self.request.GET.get("sort", "")
        sort_column = self.request.GET.get("sort", "").replace("-", "")
        order_by_list = self.default_order_by_list
        if hasattr(model, "row_number_over_%s" % sort_column):
            order_by_list = ["row_number_over_%s" % sort_column]
        return order_by_list

    def get_details_sort_menu_item_list(self):
        return self.get_details_menu_item_list('sort',SORT_ITEM_LIST)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_data = context.get('context_data',{})
        details = context_data.get('details',{})
        details.update(
            sort={
                'menu_item_list':self.get_details_sort_menu_item_list()
            },
        )
        context_data['details'] = details
        context['context_data'] = context_data
        return context
