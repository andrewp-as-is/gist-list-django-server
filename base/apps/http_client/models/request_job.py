__all__ = ["AbstractRequestJob", "RequestJob"]

import json
import os

from django.db import models

from ..utils import get_timestamp
from .mixins import HeadersMixin


class AbstractRequestJob(HeadersMixin, models.Model):
    id = models.BigAutoField(primary_key=True)
    host = models.CharField(max_length=255, help_text="used for load balancing")
    url = models.CharField(max_length=255)
    method = models.CharField(default="GET", max_length=255)
    data = models.TextField(null=True)
    headers = models.TextField(null=True)
    allow_redirects = models.BooleanField(default=True)
    disk_path = models.CharField(null=True, max_length=1024)
    redirects_limit = models.IntegerField(null=True, default=5)
    timeout = models.IntegerField(null=True)
    priority = models.IntegerField(null=True, default=0)
    retries_limit = models.IntegerField(null=True, default=1)
    created_at = models.FloatField(null=True, default=get_timestamp)

    class Meta:
        abstract = True

    def get_data(self):
        return json.loads(self.data) if self.data else {}


class RequestJob(AbstractRequestJob):
    class Meta:
        managed = False
