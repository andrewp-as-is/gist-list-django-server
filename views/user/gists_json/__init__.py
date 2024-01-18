from django.http import HttpResponse
from django.shortcuts import redirect

from views.user.public import View as _View

class View(_View):
    paginate_by = 100000

    def get(self, request, *args, **kwargs):
        qs = list(self.get_queryset() )
        # todo: .only()
        content = str(len(qs))
        response = HttpResponse(content,content_type="application/json")
        return response
