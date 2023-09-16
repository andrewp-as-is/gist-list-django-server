__all__ = ['Job']

from django.db import models

from base.apps.http_request.models import AbstractJob


class Job(AbstractJob):

    class Meta:
        managed = False

