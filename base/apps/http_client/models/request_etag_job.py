__all__ = ['RequestEtagJob']


from django.db import models


class RequestEtagJob(models.Model):
    id = models.IntegerField(primary_key=True)
    request = models.ForeignKey('Request', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
