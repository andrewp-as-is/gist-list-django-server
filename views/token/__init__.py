from datetime import datetime
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

import requests

from base.apps.github.models import Token

class View(LoginRequiredMixin,TemplateView):
    template_name = "token/index.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        token = Token.objects.get(user_id=self.request.user.id)
        url = 'https://api.github.com'
        headers = {"Authorization": "Bearer %s" % token.token}
        r = requests.head(url,headers=headers)
        if r.status_code in [200]:
            kwargs = dict(
                core_ratelimit_limit=r.headers.get('X-RateLimit-Limit'),
                core_ratelimit_remaining=r.headers.get('X-RateLimit-Remaining'),
                core_ratelimit_used=int(r.headers.get('X-RateLimit-Used')),
                core_ratelimit_reset=int(r.headers.get('X-RateLimit-Reset'))

                # updated_at=int(time.time())
            )
            Token.objects.filter(user_id=self.request.user.id).update(**kwargs)
        url = 'https://api.github.com/graphql'
        headers = {"Authorization": "Bearer %s" % token.token}
        r = requests.head(url,headers=headers)
        if r.status_code in [200]:
            kwargs = dict(
                graphql_ratelimit_limit=r.headers.get('X-RateLimit-Limit'),
                graphql_ratelimit_remaining=r.headers.get('X-RateLimit-Remaining'),
                graphql_ratelimit_used=int(r.headers.get('X-RateLimit-Used')),
                graphql_ratelimit_reset=int(r.headers.get('X-RateLimit-Reset'))
            )
            Token.objects.filter(user_id=self.request.user.id).update(**kwargs)

        self.token = Token.objects.get(id=token.id)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user.id = github.user.id
        try:
            context['token'] = Token.objects.get(user_id=self.request.user.id)
        except Token.DoesNotExist:
            pass
        return context
