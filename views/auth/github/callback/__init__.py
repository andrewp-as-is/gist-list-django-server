from django.contrib.auth import login
from django.shortcuts import redirect

from views.base import View as _View

from utils import get_github_api_data
from .utils import create_github_token, create_github_user, create_user, get_access_token


class View(_View):
    def get(self,request,*args,**kwargs):
        access_token = get_access_token(self.request.GET['code'])
        data = get_github_api_data('https://api.github.com/user',access_token)
        if not data:
            return redirect('/')
        user = create_user(data)
        create_github_user(data)
        create_github_token(data['id'],access_token)
        login(request, user, **kwargs) # signals.user_logged_in
        return redirect(user.get_absolute_url())
