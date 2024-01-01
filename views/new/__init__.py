"""
https://docs.github.com/en/rest/reference/gists#create-a-gist
"""

import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

import requests

from base.apps.github.models import Gist, Token
from base.apps.github.utils.http_response import get_disk_path

# from base.apps.http_request.models import Job as RequestJob


class View(LoginRequiredMixin, TemplateView):
    template_name = "new/new.html"

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user_id=self.request.user.id)
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
        headers = {"Authorization": "Bearer %s" % token.token}
        data = dict(public=public, description=description, files=files)
        r = requests.post(url, headers=headers, data=json.dumps(data))
        # todo: update token core ratelimit
        r.raise_for_status()
        if r.status_code in [201]:
            data = r.json()
            url = "https://api.github.com/gists/%s" % data["id"]
            headers = "\n".join(
                [
                    "Authorization: Bearer %s" % token.token,
                    "X-GitHub-Api-Version: 2022-11-28",
                ]
            )
            response_disk_path = get_disk_path(url)
            defaults = dict(
                domain="api.github.com",
                method="GET",
                headers=headers,
                response_disk_path=response_disk_path,
                priority=100,
            )
            RequestJob.objects.get_or_create(defaults, url=url)
            defaults = dict(
                owner_id=self.request.user.id,
                description=description,
                public=public,
                fork=False,
                filename_list=filename_list,
                files_count=len(files),
                forks_count=0,
                stargazers_count=0,
            )
            gist, created = Gist.objects.update_or_create(defaults, id=data["id"])
            return redirect(gist.get_absolute_url())
        return redirect("/")
