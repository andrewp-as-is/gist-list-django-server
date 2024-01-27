"""
https://gist.githubusercontent.com/andrewp-as-is/c8aed8550a9fc864884c4cd23aff5308/raw/9301662be301c874dbed38b381af0ee3215f25cd/Dockerfile
"""

__all__ = ["RawFileJob"]

from django.db import models


class RawFileJob(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField(unique=True)

    class Meta:
        db_table = 'github"."%s' % __name__.split(".")[-1]
        managed = False

    @staticmethod
    def response_match(response):
        return response.status==200 and 'https://gist.githubusercontent.com/' in response.url
