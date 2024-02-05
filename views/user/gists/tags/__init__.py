from views.base import TemplateView
from ...mixins import UserMixin

class View(UserMixin,TemplateView):
    template_name = "user/gists/tags/tag_list.html"
