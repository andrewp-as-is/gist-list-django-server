__all__ = ['RequestEtagJob']


from django.db import models


class RequestEtagJob(models.Model):
    id = models.AutoField(primary_key=True)
    request_job = models.ForeignKey('RequestJob', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
