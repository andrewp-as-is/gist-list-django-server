__all__ = ['RequestJob']


from django.db import models


class RequestJob(models.Model):
    id = models.IntegerField(primary_key=True)
    request = models.ForeignKey('Request', related_name='+',on_delete=models.DO_NOTHING)
    redirects_count = models.IntegerField(null=True, default=1)
    retries_limit = models.IntegerField(null=True, default=1)

    class Meta:
        managed = False
