from base.apps.github.models import GistStar
from base.apps.github_gist_star_matview.models import Gist as MatviewGist
from base.apps.github_gist_star_new_matview.models import Gist as NewMatviewGist
from views.user.gists import ListView


class ListView(ListView):

    def get_model(self):
        if self.github_user:
            if NewMatviewGist.objects.filter(stargazer_id=self.github_user.id).only('id').first():
                return NewMatviewGist
        return MatviewGist

    def get_queryset_base(self):
        model = self.get_model()
        if not hasattr(self,'github_user') or not self.github_user:
            return model.objects.none()
        qs = model.objects.filter(stargazer_id=self.github_user.id)
        return qs
