__all__ = ["GraphqlApiUserGistsFileJob"]

from django.db import models


class GraphqlApiUserGistsFileJob(models.Model):
    user_id = models.IntegerField()
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==200 and 'api.github.com/graphql/' in response.request.url and 'user.gists' in response.request.url