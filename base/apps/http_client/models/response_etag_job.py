__all__ = ['ResponseEtagJob']


from django.db import models


class ResponseEtagJob(models.Model):
    id = models.AutoField(primary_key=True)
    response = models.ForeignKey('Response', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
