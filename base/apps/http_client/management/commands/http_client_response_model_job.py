from urllib.parse import parse_qs, urlparse

from django.apps import apps

from base.apps.http_client.models import ResponseModelJob
from management.base import JobCommand

"""
TODO

URL_REGEX
REQUEST_URL_REGEX
RESPONSE_URL_REGEX

REQUEST_HOST_REGEX

STATUS_LIST = []
METHOD_LIST = []
"""


MODEL_LIST = list(filter(
    lambda m:hasattr(m,'response_match'),
    apps.get_models()
))

def get_user_id(url):
    if "user_id" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["user_id"][0])
    if "https://api.github.com/user/" in url:
        return int(url.replace("https://api.github.com/user/", "").split("/")[0])

def iter_model(response):
    for model in MODEL_LIST:
        if model.response_match(response):
            yield model

def get_model_kwargs(model,response):
    kwargs = {}
    if hasattr(model,'path'):
        kwargs['path'] = response.disk_path
    if hasattr(model,'url'):
        kwargs['url'] = response.url
    if hasattr(model,'response_id'):
        kwargs['response_id'] = response.id
    if hasattr(model,'user_id'):
        kwargs['user_id'] = get_user_id(response.url)
    return kwargs

class Command(JobCommand):

    def do_job(self, job):
        for model in iter_model(job.response):
            kwargs = get_model_kwargs(model,job.response)
            self.create(model(**kwargs))
            self.MODEL2BULK_CREATE_KWARGS[model] = dict(ignore_conflicts=True)
