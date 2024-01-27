from views.base import TemplateView
from ..mixins import GistMixin


class View(GistMixin,TemplateView):
    template_name = 'user/gist/clone.html'
