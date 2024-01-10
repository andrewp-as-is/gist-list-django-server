__all__ = ["ApiRateLimitHeadersJob"]

from django.db import models


class ApiRateLimitHeadersJob(models.Model):
    id = models.AutoField(primary_key=True)
    response = models.OneToOneField('http_client.Response', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return True
