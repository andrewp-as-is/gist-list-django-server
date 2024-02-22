__all__ = [
    "AbstractResponse",
    "Response",
]

import json
import os

import shutil

from django.conf import settings
from django.db import models


class AbstractResponse(models.Model):
    id = models.BigAutoField(primary_key=True)
    request = models.ForeignKey('http_client.Request', related_name='+',on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=255)
    status = models.IntegerField()
    headers = models.TextField(null=True)
    created_at = models.FloatField()

    class Meta:
        abstract = True

    def get_disk_path(self):
        return os.path.join(settings.HTTP_RESPONSE_DIR,self.request.disk_relpath)

    def get_content(self):
        path = self.get_disk_path()
        if os.path.exists(str(path)):
            return open(path).read()

    def get_content_data(self):
        content = self.get_content()
        if content:
            return json.loads(content)

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
