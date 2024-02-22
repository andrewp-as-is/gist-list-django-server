from django.shortcuts import redirect

from base.apps.homepage.models import User
from views.base import ListView

class View(ListView):
    context_object_name = "user_list"
    template_name = "frontpage/user_list.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/%s' % request.user.login)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.all().order_by('order')
