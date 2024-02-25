__all__ = [
    "AbstractResponse",
    "Response",
]

import io
import json
from http.client import parse_headers
import os

import shutil

from django.db import models

from base import settings
from .mixins import HeadersMixin

class AbstractResponse(HeadersMixin,models.Model):
    id = models.BigAutoField(primary_key=True)
    request = models.ForeignKey('http_client.Request', related_name='+',on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=255)
    status = models.IntegerField()
    headers = models.TextField(null=True)
    created_at = models.FloatField()

    class Meta:
        abstract = True

    def get_dir_path(self):
        return os.path.join(settings.HTTP_CLIENT_DIR,self.request.response_dir_relpath)

    def get_content_path(self):
        dir_path = self.get_dir_path()
        return os.path.join(dir_path,'content')

    def get_headers_path(self):
        dir_path = self.get_dir_path()
        return os.path.join(dir_path,'headers')

    def get_content(self):
        content_path = self.get_content_path()
        if os.path.exists(str(content_path)):
            return open(content_path).read()

    def get_content_data(self):
        content = self.get_content()
        if content:
            return json.loads(content)

    def get_headers(self):
        path = self.get_headers_path()
        fp = io.BytesIO(open(path).read().encode())
        return dict(parse_headers(fp)) if fp else {}

    def delete_disk_path(self):
        path = self.get_disk_path()
        if os.path.exists(path):
            if os.path.isfile(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)


class Response(AbstractResponse):
    class Meta:
        managed = False
