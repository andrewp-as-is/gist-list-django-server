from views.base import TemplateView
from ...mixins import UserMixin

class View(UserMixin,TemplateView):
    template_name = "user/gists/languages/language_list.html"
