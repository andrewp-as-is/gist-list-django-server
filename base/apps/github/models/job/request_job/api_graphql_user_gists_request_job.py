__all__ = ['ApiGraphqlUserGistsRequestJob']

from django.db import models

class ApiGraphqlUserGistsRequestJob(models.Model):
    user_id = models.TextField()

    class Meta:
        managed = False
