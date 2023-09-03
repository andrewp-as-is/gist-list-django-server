from django.views.generic.base import TemplateView
from views.user.mixins import UserMixin

class ScriptsView(UserMixin,TemplateView):
    template_name = "user/scripts/scripts.html"
