__all__ = ['AbstractResponse','Response',]

import http.client
from http.client import parse_headers
import io
import json
import logging
import os
import orjson
import shutil

from django.db import models

from ..utils import get_path, get_timestamp

http.client._MAXHEADERS = 42

class AbstractResponse(models.Model):
    domain = models.TextField()
    url = models.TextField()
    status = models.IntegerField()
    relpath = models.TextField(null=True) # hardcoded path to prevent endless loop disk overflow
    content_size = models.IntegerField(null=True)
    job_priority = models.IntegerField(null=True)
    timestamp = models.IntegerField(default=get_timestamp)

    class Meta:
        abstract = True

    def get_path(self):
        return get_path(self.relpath)

    def get_content_relpath(self):
        return os.path.join(self.relpath,'content')

    def get_headers_relpath(self):
        return os.path.join(self.relpath,'headers')

    def get_request_headers_relpath(self):
        return os.path.join(self.relpath,'request_headers')

    def get_content_path(self):
        return get_path(self.get_content_relpath())

    def get_headers_path(self):
        return get_path(self.get_headers_relpath())

    def get_request_headers_path(self):
        return get_path(self.get_request_headers_relpath())

    def get_content(self):
        path = get_path(self.get_content_relpath())
        if path:
            return open(path).read()

    def get_data(self):
        path = get_path(self.get_content_relpath())
        if path:
            # return json.load(open(path))
            return orjson.loads(open(path).read())

    def get_headers(self):
        path = get_path(self.get_headers_relpath())
        if path and os.path.exists(path):
            fp = io.BytesIO(open(path).read().encode())
            return dict(parse_headers(fp)) if fp else {}
        return {}

    def get_request_headers(self):
        path = get_path(self.get_request_headers_relpath())
        if path and os.path.exists(path):
            # return get_headers(open(path).read().encode())
            fp = io.BytesIO(open(path).read().encode())
            return dict(parse_headers(fp)) if fp else {}
        return {}

    def get_etag(self):
        for k,v in self.get_headers().items():
            if k.lower()=='etag':
                return v

    def delete_files(self):
        path = self.get_path()
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                logging.error(e)

class Response(AbstractResponse):

    class Meta:
        managed = False
