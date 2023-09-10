from views.user.gists import View as ListView
from .utils import get_starred_gist_model

class View(ListView):

    def get_model(self):
        if self.github_user:
            return get_starred_gist_model(self.github_user.id)
        return Gist.objects.none()

    def get_queryset_base(self):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        qs = model.objects.filter(stargazer_id=self.github_user.id)
        return qs
