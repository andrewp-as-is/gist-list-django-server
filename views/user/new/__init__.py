"""
https://docs.github.com/en/rest/reference/gists#create-a-gist
"""

import json
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from views.base import TemplateView

import requests

from base.apps.github.models import Gist, GistOrderJob, Token, UserTableModification, UserStat
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
        filename_list, language_list, raw_url_list = [], [], []
        for filename, file_data in d["files"].items():
            filename_list += [filename]
            language_list += [file_data["language"]]
            raw_url_list+=[file_data["raw_url"]]
        language_list = list(sorted(set(filter(None, language_list))))
        create_obj_list = [
            Gist( # github.gist
                id=data["id"],
                owner_id=user_id,
                description=description,
                public=public,
                fork=False,
                filename_list=filename_list,
                language_list=language_list,
                raw_url_list=raw_url_list,
                stargazers_count=0,
                forks_count=0,
                created_at=timestamp,
                updated_at=timestamp
            ),
            GistOrderJob(user_id=user_id),
            RefreshJob(schemaname='github_live_matview',matviewname='gist'),
            UserTableModification(
                user_id=user_id,tablename='gist',modified_at=timestamp
            )
        ]
        with transaction.atomic():
            for obj in create_obj_list:
                type(obj).models.bulk_create([obj],ignore_conflicts=True)
            UserTableModification.objects.filter(
                user_id=user_id,tablename='gist'
            ).update(modified_at=timestamp)
            self.execute_sql('CALL github.gist_order_job()')
            # todo: UserStat
        url = '/%s/%s' % (self.request.user.login,data["id"])
        return redirect(url)
