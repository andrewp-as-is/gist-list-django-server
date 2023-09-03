from django.contrib.auth import logout
from django.shortcuts import redirect

from base.apps.github.models import Token
from views.base import View as _View

"""
from django.contrib.auth.views import LogoutView

path('logout', LogoutView.as_view(
    next_page=(getattr(settings,'LOGOUT_REDIRECT_URL','/') or '/')
))
"""

class View(_View):

    def get(self, request):
        Token.objects.filter(user_id=request.user.id).delete()
        response = logout(request)
        return redirect('/')
