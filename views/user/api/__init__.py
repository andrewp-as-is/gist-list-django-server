from django.views.generic.base import TemplateView
from views.user.mixins import UserMixin

class View(UserMixin,TemplateView):
    template_name = "user/api/api.html"
