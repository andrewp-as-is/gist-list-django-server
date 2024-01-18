from views.base import TemplateView
from views.user.gist.mixins import GistMixin


class View(GistMixin,TemplateView):
    template_name = 'user/gist/clone.html'
