from views.user.gists.tags import View as _View
from ..utils import get_gist_star_model

class View(_View):

    def get_gist_queryset(self):
        gist_model = get_gist_star_model(self.github_user.id)
        return gist_model.objects.filter(stargazer_id=self.github_user.id)
