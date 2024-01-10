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
    lambda m:m!=ResponseModelJob and '_job' in m._meta.db_table,
    apps.get_models()
))

def get_user_id(url):
    if "user_id" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["user_id"][0])
    if "https://api.github.com/user/" in url:
        return int(url.replace("https://api.github.com/user/", "").split("/")[0])

def get_model(response):
    for model in MODEL_LIST:
        if hasattr(model,'response_match'):
            print('%s: %s' % (model,response.url))
            if model.response_match(response):
                return model
    print('UNKNOWN MODEL: %s' % (response.url))

def get_model_kwargs(model,response):
    kwargs = {}
    if hasattr(model,'path'):
        kwargs['path'] = response.disk_path
    if hasattr(model,'url'):
        kwargs['url'] = response.url
    if hasattr(model,'response_id'):
        kwargs['response_id'] = response.id
    user_id = get_user_id(response.url)
    if hasattr(model,'user_id') and user_id:
        kwargs['user_id'] = user_id
    return kwargs

class Command(JobCommand):

    def do_job(self, job):
        model = get_model(job.response)
        if model:
            kwargs = get_model_kwargs(model,job.response)
            self.create(model(**kwargs))
            self.MODEL2BULK_CREATE_KWARGS[model] = dict(ignore_conflicts=True)
        else:
            print('UNKNOWN MODEL: %s' % job.response.url)
