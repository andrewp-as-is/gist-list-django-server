from django.http import HttpResponse

from views.base import View as _View

class View(_View):
    def get(self,request):
        return HttpResponse(open('robots.txt').read())
