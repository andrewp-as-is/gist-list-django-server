__all__ = ["ResponseJob"]

from django.db import models


class ResponseJob(models.Model):
    id = models.IntegerField(primary_key=True)
    response_id = models.IntegerField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False
