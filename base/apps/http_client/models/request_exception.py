__all__ = [
    "AbstractRequestException",
    "RequestException",
]

from django.db import models


class AbstractRequestException(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey('Request', related_name='+',on_delete=models.DO_NOTHING)
    exc_class = models.TextField()
    exc_message = models.TextField()
    created_at = models.FloatField()

    class Meta:
        abstract = True


class RequestException(AbstractRequestException):

    class Meta:
        managed = False
