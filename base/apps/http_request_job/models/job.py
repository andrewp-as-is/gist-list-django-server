__all__ = ['AbstractJob','Job']

from http.client import parse_headers
import io
import os

from django.db import models

from base.conf import RESPONSE_DIRNAME


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        return super().bulk_create(objs,
            update_conflicts=True,
            unique_fields = ['url',],
            update_fields = ['headers','data','priority']
        )

class AbstractJob(models.Model):
    objects = Manager()

    domain = models.CharField(max_length=255)
    url = models.CharField(unique=True,max_length=255)
    method = models.CharField(default='GET',max_length=255)
    data = models.TextField(null=True)
    headers = models.TextField(null=True)
    allow_redirects = models.BooleanField(default=True)
    response_relpath = models.TextField(null=True)
    attempts_count = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def get_headers(self):
        if self.headers:
            fp = io.BytesIO(self.headers.encode())
            return dict(parse_headers(fp)) if fp else {}
        return {}

    def get_response_path(self):
        return os.path.join(RESPONSE_DIRNAME,response_relpath)

class Job(AbstractJob):
    objects = Manager()

    class Meta:
        managed = False
