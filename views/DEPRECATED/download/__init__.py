"""
/download?user=LOGIN&gist=ID&filename=FILENAME
"""

from django.http import HttpResponse

from django.shortcuts import redirect
import requests

from base.apps.github.models import Gist
from views.base import View as _View

class View(_View):

    def get(self, request, *args, **kwargs):
        gist_id = self.request.GET.get('gist','')
        filename = self.request.GET.get('filename','')
        try:
            gist = Gist.objects.get(id=gist_id)
        except Gist.DoesNotExist:
            return HttpResponse('gist %s not found' % gist_id, status=404)
        filename2raw_url = gist.filename2raw_url
        raw_url = filename2raw_url.get(filename,None)
        if not raw_url:
            return HttpResponse('%s not found' % filename, status=404)
        r = requests.get(url=raw_url)
        if r.status_code!=200:
            return HttpResponse(r.text, status=r.status_code)
        response = HttpResponse(r.text,content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
