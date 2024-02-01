from ...utils import get_gist_star_model, get_starred_gist_model
from .. import View as _View


class View(_View):

    def get_model(self):
        return get_starred_gist_model(self.github_user_stat)

    def get_queryset_base(self):
        model = self.get_model()
        gist_star_model = get_gist_star_model(self.github_user_stat)
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        qs = model.objects.filter(
            id__in=gist_star_model.objects.filter(user_id=self.github_user.id).values_list('gist_id',flat=True)
        )
        return qs

    def get_queryset(self, **kwargs):
        model = self.get_model()
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
