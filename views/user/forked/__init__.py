from base.apps.github.models import Gist
from views.user.gists import ListView

class ListView(ListView):
    template_name = "user/gists/gist_list.html"

    def get_queryset_base(self):
        if not hasattr(self,'github_user') or not self.github_user:
            return Gist.objects.none()
        qs = Gist.objects.filter(owner_id=self.github_user.id,is_fork=True)
        if not self.request.user.is_authenticated or self.github_user.login != self.request.user.login:
            qs = qs.filter(is_public=True)
        return qs
