from views.user.gists import View as ListView
from utils import get_starred_gist_model

class View(ListView):

    def get_model(self):
        return get_starred_gist_model(self.modification_matview_time)

    def get_queryset_base(self):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        qs = model.objects.filter(stargazer_id=self.github_user.id)
        return qs

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
       # if hasattr(model,'starred_order'):
        #    qs = qs.select_related('owner')
        order_by_list = self.get_queryset_order_by_list()
        return qs.order_by(*order_by_list)

    def get_queryset_order_by_list(self,**kwargs):
        sort = self.request.GET.get('sort','')
        sort_prefix = '-' if sort and sort[0]=='-' else ''
        sort_column = self.request.GET.get('sort','').replace('-','')
        order_by = ['starred_order']
        return order_by
