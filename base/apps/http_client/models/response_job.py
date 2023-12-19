__all__ = ['ResponseJob']


from django.db import models


class ResponseJob(models.Model):
    request = models.ForeignKey('Request', related_name='+',on_delete=models.DO_NOTHING)
    response = models.ForeignKey('Response', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
