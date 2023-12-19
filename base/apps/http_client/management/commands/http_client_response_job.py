from urllib.parse import parse_qs, urlparse

from base.apps.http_client.models import ResponseJob
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
    lambda m:m!=ResponseJob and '_job' in m._meta.db_table,
    apps.get_models()
))

def get_user_id(url):
    if "user_id" in url:
        parsed_url = urlparse(url)
        return int(parse_qs(parsed_url.query)["user_id"][0])
    if "https://api.github.com/user/" in url:
        return int(url.replace("https://api.github.com/user/", "").split("/")[0])


def response_match(model,response):
    return False

def get_model(response):
    for model in MODEL_LIST:
        if hasattr(model,'response_match'):
            if model.response_match(response):
                return True
        if response_match(model,response):
            return model
    return model

def get_model_kwargs(model,response):
    kwargs = {}
    if hasattr(model,'path'):
        kwargs['path'] = response.disk_path
    if hasattr(model,'url'):
        kwargs['url'] = response.request.url
    if hasattr(model,'request_id'):
        kwargs['request_id'] = response.request_id
    if hasattr(model,'response_id'):
        kwargs['response_id'] = response.id
    user_id = get_user_id(response.request.url)
    if user_id:
        kwargs['user_id'] = user_id
    return kwargs

class Command(JobCommand):

    def do_job(self, response):
        model = get_model(response)
        kwargs = get_model_kwargs(model,response)
        self.create(model(**kwargs))
