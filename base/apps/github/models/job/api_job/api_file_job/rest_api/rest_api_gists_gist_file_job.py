__all__ = ["RestApiGistsGistFileJob"]

from django.db import models


class RestApiGistsGistFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True

    @staticmethod
    def response_match(response):
        return response.status==200 and 'gists/' in response.url and response.url.split('/')[-1].isdigit()
