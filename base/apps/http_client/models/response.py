__all__ = [
    "AbstractResponse",
    "Response",
]

import json
import os

import shutil

from django.db import models

from ..utils import get_headers, get_timestamp
from .mixins import HeadersMixin


class AbstractResponse(HeadersMixin, models.Model):
    id = models.BigAutoField(primary_key=True)
    request = models.ForeignKey('Request', related_name='+',on_delete=models.DO_NOTHING)
    host = models.CharField(max_length=255) # todo: remove?
    url = models.CharField(max_length=255) # todo: remove?
    status = models.IntegerField()
    headers = models.TextField(null=True)
    created_at = models.FloatField(default=get_timestamp)

    class Meta:
        abstract = True

    def get_content(self):
        disk_path_list = [
            self.disk_path,
            os.path.join(str(self.disk_path), "content"),
        ]
        for disk_path in disk_path_list:
            if os.path.exists(str(disk_path)):
                return open(disk_path).read()

    def get_content_data(self):
        content = self.get_content()
        if content:
            return json.loads(content)

    def delete_disk_path(self):
        if os.path.exists(self.disk_path):
            if os.path.isfile(self.disk_path):
                os.unlink(self.disk_path)
            else:
                shutil.rmtree(self.disk_path)


class Response(AbstractResponse):
    class Meta:
        managed = False
