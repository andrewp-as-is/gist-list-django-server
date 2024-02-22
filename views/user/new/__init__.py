"""
https://docs.github.com/en/rest/reference/gists#create-a-gist
"""

import json
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect
from views.base import TemplateView

import requests

from base.apps.github.models import Gist, UserGistRowNumberJob, Token, UserPublicStat, AuthenticatedUserStat
from ..mixins import UserMixin


class View(LoginRequiredMixin,UserMixin,TemplateView):
    template_name = "user/new/new.html"

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        token = Token.objects.get(user_id=user_id)
        public = request.POST.get("gist[public]") == "1"
        description = request.POST.get("gist[description]")
        names = request.POST.getlist("gist[contents][][name]")
        values = request.POST.getlist("gist[contents][][value]")
        files = {}
        filename_list = []
        for i, name in enumerate(names):
            filename_list += [name]
            files[name] = dict(content=values[i], filename=names[i])
        url = "https://api.github.com/gists"
        headers = {
            "Authorization": "Bearer %s" % token.token,
            "X-GitHub-Api-Version": "2022-11-28"
        }
        data = dict(public=public, description=description, files=files)
        r = requests.post(url, headers=headers, data=json.dumps(data),timeout=5)
        if r.status_code not in [201]:
            return HttpResponse(r.text, status=r.status_code)
        timestamp = round(time.time(),3)
        data = r.json()
        filename_list, language_list, raw_url_hash_list = [], [], []
        for filename, file_data in data["files"].items():
            filename_list += [filename]
            language_list += [file_data["language"]]
            # https://gist.githubusercontent.com/USER/GIST/raw/HASH/FILENAME
            raw_url_hash = file_data["raw_url"].split('/')[-2]
            raw_url_hash_list+=[raw_url_hash]
        language_list = list(sorted(set(filter(None, language_list))))
        defaults = dict(
            owner_id=user_id,
            description=description,
            public=public,
            fork=False,
            filename_list=filename_list,
            language_list=language_list,
            raw_url_hash_list=raw_url_hash_list,
            stargazers_count=0,
            forks_count=0,
            created_at=timestamp,
            updated_at=timestamp
        )
        gist, created = Gist.objects.get_or_create(defaults,id=data['id'])
        # todo: github.gist_file
        # secret_gists_count=F('secret_gists_count') + 1
        gist_queryset = Gist.objects.filter(owner_id=user_id)
        # todo: user_table
        UserPublicStat.objects.filter(user_id=user_id).update(
            gists_count=gist_queryset.filter(public=True).count()
        )
        AuthenticatedUserStat.objects.filter(user_id=user_id).update(
            gists_count=gist_queryset.count()
        )
        UserGistRowNumberJob.objects.get_or_create(user_id=user_id)
        return redirect(gist.get_absolute_url())
