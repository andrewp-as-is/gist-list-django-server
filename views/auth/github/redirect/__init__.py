from django.shortcuts import redirect
from views.base import View as _View

from .utils import get_url

class View(_View):
    def get(self,request,*args,**kwargs):
        return redirect(get_url())
