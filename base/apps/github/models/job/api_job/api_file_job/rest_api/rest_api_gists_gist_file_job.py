__all__ = ["RestApiGistsGistFileJob"]

from django.db import models


class RestApiGistsGistFileJob(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True

    def response_match(self,response):
        return response.status==200 and 'gists/' in response.request.url and response.request.url.split('/')[-1].isdigit()
