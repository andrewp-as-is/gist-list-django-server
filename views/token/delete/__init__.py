from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from base.apps.github.models import Token
from views.base import View as _View

class View(LoginRequiredMixin,_View):

    def get(self, request):
        Token.objects.filter(user_id=request.user.id).delete()
        return redirect('/token')
