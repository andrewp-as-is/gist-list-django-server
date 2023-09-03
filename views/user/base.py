from django.http import HttpResponse

from base.apps.github.models import Gist
from views.base import View as _View
from .mixins import UserMixin

class LinesView(UserMixin,View):
    content_type = 'text/plain'

    def get_queryset(self):
        return Gist.objects.filter(owner_id=self.github_user.id).order_by('id')

    def get(self,request,*args,**kwargs):
        self.qs = self.get_queryset()
        response = HttpResponse("\n".join(self.iter_lines()), content_type=self.content_type)
        return response
