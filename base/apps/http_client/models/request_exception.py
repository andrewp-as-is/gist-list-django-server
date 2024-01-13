__all__ = [
    "AbstractReqestException",
    "ReqestException",
]

from django.db import models


class AbstractReqestException(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField()
    exc_class = models.TextField()
    exc_message = models.TextField()
    created_at = models.FloatField()

    class Meta:
        abstract = True


class ReqestException(AbstractReqestException):

    class Meta:
        managed = False
