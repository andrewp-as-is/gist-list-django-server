"""
wget -q https://gist.github.com/<LOGIN>/<ID>/archive/<VERSION>.zip -O <ID>.zip
"""

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from base.apps.github.models import User
from views.base import View as _View
from views.utils import get_gist_model

FILENAME = 'gist-wget.sh'

class View(_View):
    def get(self,request):
        login = request.GET.get('login','')
        github_user = get_object_or_404(User, login=login)
        model = get_gist_model(github_user.id)
        gist_list = list(model.objects.filter(owner_id=github_user.id).only('id','version','owner__id','owner__login').select_related('owner'))
        line_list = []
        if request.GET.get('download',''):
            line_list = ['#!/usr/bin/env bash','']
        for gist in gist_list:
            if gist.version:
                url = 'https://gist.github.com/%s/%s/archive/%s.zip' % (
                    gist.owner.login,gist.id,gist.version
                )
            else:
                url = '# https://gist.github.com/%s/%s/archive/None.zip' % (
                    gist.owner.login,gist.id
                )
            line_list+=['set -x; wget -q %s -O %s.zip;' % (url,gist.id)]
        response = HttpResponse("\n".join(line_list),content_type="text/plain")
        if request.GET.get('download',''):
            response['Content-Disposition'] = 'attachment; filename=%s' % FILENAME
        return response
