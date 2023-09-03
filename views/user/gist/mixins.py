from base.apps.github.models import Gist
from views.user.mixins import UserMixin

class GistMixin(UserMixin):
    def dispatch(self, *args, **kwargs):
        self.gist = Gist.objects.get(pk=self.kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gist'] = self.gist
        return context

