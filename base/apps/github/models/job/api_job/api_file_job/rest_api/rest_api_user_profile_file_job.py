__all__ = ["RestApiUserProfileFileJob"]

from django.db import models


class RestApiUserProfileFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return response.status==200 and '/user/' in response.url and response.url.split('/')[-1].split('?')[0].isdigit()
