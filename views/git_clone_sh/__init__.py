"""
git clone -q git@gist.github.com:<ID>.git
git clone -q https://gist.github.com/<ID>.git
"""

from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.views.generic.base import View as _View
from base.apps.github.models import User
# from views.utils import get_gist_model

FILENAME = 'gist-clone.sh'

class View(_View):
    def get(self,request):
        login = request.GET.get('login','')
        protocol = request.GET.get('protocol','ssh')
        download = request.GET.get('download','')
        user = get_object_or_404(User, login=login)
        model = get_gist_model(user.id)
        gist_list = list(model.objects.filter(owner_id=user.id).only('id'))
        line_list = []
        if download:
            line_list = ['#!/usr/bin/env bash','']
        for gist in gist_list:
            url = 'https://gist.github.com/%s.git' % gist.id
            if protocol=='ssh':
                url = 'git@gist.github.com:%s.git' % gist.id
            line_list+=['set -x; git clone -q %s' % url]
        response = HttpResponse("\n".join(line_list),content_type="text/plain")
        if download:
            response['Content-Disposition'] = 'attachment; filename=%s' % FILENAME
        return response
