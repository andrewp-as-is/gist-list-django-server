__all__ = ["GraphqlApiCursorJob"]

from django.db import models


class GraphqlApiCursorJob(models.Model):
    id = models.AutoField(primary_key=True)
    response = models.OneToOneField('http_client.Response', related_name='+',on_delete=models.DO_NOTHING)
    token = models.OneToOneField('TokenBase', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return 'api.github.com/graphql' in response.url
