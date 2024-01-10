__all__ = ["RestApiViewerGistsFileJob"]

from django.db import models


class RestApiViewerGistsFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    path = models.TextField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return response.status==200 and '/gists?' in response.url
