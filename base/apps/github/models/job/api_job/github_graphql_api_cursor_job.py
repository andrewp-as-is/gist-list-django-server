__all__ = ["GithubGraphqlApiCursorJob"]

from django.db import models


class GithubGraphqlApiCursorJob(models.Model):
    id = models.IntegerField(primary_key=True)
    request = models.ForeignKey('http_client.Request', related_name='+',on_delete=models.DO_NOTHING)
    response = models.OneToOneField('http_client.Response', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return 'api.github.com/graphql/' in response.request.url
