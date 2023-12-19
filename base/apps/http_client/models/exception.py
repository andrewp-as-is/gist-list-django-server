__all__ = [
    "AbstractException",
    "ExceptionModel",
]

from django.db import models

from .mixins import RequestInfoMixin


class AbstractException(RequestInfoMixin, models.Model):
    request_info = models.TextField()
    exc_class = models.TextField()
    exc_message = models.TextField()
    created_at = models.FloatField()

    class Meta:
        abstract = True


class ExceptionModel(AbstractException):
    class Meta:
        managed = False
