from views.user.gists import View as _View

class View(_View):

    def get_queryset_base(self):
        self.gist_model
        if not hasattr(self,'github_user') or not self.github_user:
            return self.gist_model.objects.none()
        qs = self.gist_model.objects.filter(owner_id=self.github_user.id).filter(public=True)
        return qs
