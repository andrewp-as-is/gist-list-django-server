from .. import View as _View

class View(_View):

    def get_queryset_base(self):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        qs = model.objects.filter(owner_id=self.github_user.id).filter(public=True)
        return qs
