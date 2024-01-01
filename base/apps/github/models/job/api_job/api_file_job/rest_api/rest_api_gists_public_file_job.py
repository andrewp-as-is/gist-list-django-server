__all__ = ["RestApiGistsPublicFileJob"]

from django.db import models


class RestApiGistsPublicFileJob(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True

    def response_match(self,response):
        return response.status==200 and 'gists/public' in response.request.url
