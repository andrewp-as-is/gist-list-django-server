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
        id_list = list(model.objects.filter(owner_id=user.id).values_list('id',flat=True))
        response = HttpResponse("\n".join(id_list),content_type="text/plain")
        if request.GET.get('download',''):
            response['Content-Disposition'] = 'attachment; filename=gist-id.txt'
        return response
