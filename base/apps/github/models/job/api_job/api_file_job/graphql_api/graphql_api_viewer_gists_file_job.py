__all__ = ["GraphqlApiViewerGistsFileJob"]

from django.db import models


class GraphqlApiViewerGistsFileJob(models.Model):
    response_id = models.IntegerField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    def response_match(self,response):
        return response.status==200 and 'api.github.com/graphql/' in response.request.url and 'viewer.gists' in response.request.url
