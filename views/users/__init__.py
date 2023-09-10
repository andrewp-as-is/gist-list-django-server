from django.shortcuts import redirect

from base.apps.github_matview.models import User
from views.base import ListView

class View(ListView):
    context_object_name = "user_list"
    template_name = "users/user_list.html"

    def get_queryset(self):
        return User.objects.all().order_by('id')
