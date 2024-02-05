from ...utils import get_gist_star_model
from .. import View as _View


class View(_View):
    context_object_name = "gist_star_list"
    template_name = "user/starred/gist_star_list.html"
    default_order_by_list = ["-row_number_over_starred"]

    def get_model(self):
        return get_gist_star_model(self.github_user_stat)

    def get_queryset_base(self):
        # todo: gist_star remake
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        # id__in=gist_star_model.objects.filter(user_id=self.github_user.id).values_list('gist_id',flat=True)
        qs = model.objects.filter(user_id=self.github_user.id) #.select_related()
        return qs

    def get_queryset(self, **kwargs):
        model = self.get_model()
        qs = super().get_queryset(**kwargs)
       # if hasattr(model,'starred_order'):
        #    qs = qs.select_related('owner')
        order_by_list = self.get_queryset_order_by_list()
        return qs.order_by(*order_by_list)
