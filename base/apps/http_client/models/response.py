__all__ = [
    "AbstractResponse",
    "Response",
]

import json
import os

import shutil

from django.db import models

from .mixins import HeadersMixin


class AbstractResponse(HeadersMixin, models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)
    status = models.IntegerField()
    headers = models.TextField(null=True)
    disk_path = models.TextField(null=True)
    created_at = models.FloatField()

    class Meta:
        abstract = True

    def get_content(self):
        if os.path.exists(str(self.disk_path)):
            return open(self.disk_path).read()

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
