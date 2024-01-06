from views.user.gists.tags import View as _View

class View(_View):

    def get_gist_queryset(self):
        return self.gist_star_model.objects.filter(stargazer_id=self.github_user.id)
