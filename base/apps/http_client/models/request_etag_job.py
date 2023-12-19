__all__ = ['RequestEtagJob']


from django.db import models


class RequestEtagJob(models.Model):
    request = models.ForeignKey('Request', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
