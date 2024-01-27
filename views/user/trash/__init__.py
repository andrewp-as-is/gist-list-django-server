from base.apps.github.models import Trash
from views.base import ListView
from ..mixins import UserMixin

class View(UserMixin, ListView):
    model = Trash
    context_object_name = "trash_list"
    template_name = "user/trash/trash_list.html"

    def get(self, request, *args, **kwargs):
        login = self.kwargs.get("login")
        if request.path == "/%s/" % login:
            return redirect("/%s" % login)
        return super().get(request, *args, **kwargs)

    def get_queryset_base(self, **kwargs):
        if (
            not hasattr(self, "github_user")
            or not self.github_user
            or not self.github_user_refresh
        ):
            return self.gist_model.objects.none()
        qs = self.gist_model.objects.filter(owner_id=self.github_user.id)
        if (
            not self.request.user.is_authenticated
            or self.github_user.login != self.request.user.login
        ):
            qs = qs.filter(public=True)
        return qs

    def get_queryset(self, **kwargs):
        model = self.model
        if (
            not hasattr(self, "github_user")
            or not self.github_user
            or not self.github_user_refresh
        ):
            return model.objects.none()
        return model.objects.all()
