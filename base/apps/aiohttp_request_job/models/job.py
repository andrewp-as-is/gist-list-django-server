__all__ = ['Job']

from django.db import models

from base.apps.http_request_job.models import AbstractJob


class Job(AbstractJob):

    class Meta:
        managed = False

