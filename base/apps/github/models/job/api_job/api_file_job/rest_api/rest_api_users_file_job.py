__all__ = ["RestApiUsersFileJob"]

from django.db import models


class RestApiUsersFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.TextField()

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = True

    @staticmethod
    def response_match(response):
        return response.status==200 and '/users' in response.url
