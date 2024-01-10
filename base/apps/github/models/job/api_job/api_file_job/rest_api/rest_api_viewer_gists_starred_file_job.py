__all__ = ["RestApiViewerGistsStarredFileJob"]

from django.db import models


class RestApiViewerGistsStarredFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    path = models.TextField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return response.status==200 and '/gists/starred?' in response.url
