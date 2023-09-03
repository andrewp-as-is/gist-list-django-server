from django.shortcuts import redirect

from django.views.generic.base import View as _View

class View(_View):
    def get(self,request):
        login = request.GET.get('q','')
        url = '/%s' % login if login else ''
        return redirect(url)
