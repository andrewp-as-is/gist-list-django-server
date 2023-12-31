from django.shortcuts import get_object_or_404

from base.apps.github.models import Gist, GistRefresh
from views.user.mixins import UserMixin


class GistMixin(UserMixin):
    def dispatch(self, *args, **kwargs):
        self.gist = get_object_or_404(Gist, pk=self.kwargs["pk"])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gist"] = self.gist
        context["gist_user_refresh"] = (
            GistRefresh.objects.filter(gist_id=self.gist.id).count() > 0
        )
        return context
