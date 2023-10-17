from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from base.apps.github.models import User
from views.base import View as _View
# from views.utils import get_gist_model

class View(_View):
    def get(self,request):
        login = request.GET.get('login','')
        user = get_object_or_404(User, login=login)
        model = get_gist_model(user.id)
        gist_list = list(model.objects.filter(owner_id=user.id,version__isnull=False).only('id','version','owner__id','owner__login').select_related('owner'))
        line_list = list(map(
            lambda g:'https://gist.github.com/%s/%s/archive/%s.zip' % (g.owner.login,g.id,g.version),
            gist_list
        ))
        response = HttpResponse("\n".join(line_list),content_type="text/plain")
        if request.GET.get('download',''):
            response['Content-Disposition'] = 'attachment; filename=download.txt'
        return response
