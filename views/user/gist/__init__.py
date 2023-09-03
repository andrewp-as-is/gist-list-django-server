from base.apps.github.models import Gist, GistStar
from django.views.generic.base import TemplateView
from .mixins import GistMixin

class DetailView(GistMixin,TemplateView):
    model = Gist
    template_name = "user/gist/gist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['starred_gist'] = GistStar.objects.get(
                    gist_id=self.kwargs['pk'],
                    user_id=self.request.user.id
                )
            except GistStar.DoesNotExist:
                pass
        return context
