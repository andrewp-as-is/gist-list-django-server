__all__ = ['ApiUsersResponseJob']

from django.db import models

class ApiUsersResponseJob(models.Model):
    response_id = models.IntegerField()

    class Meta:
        managed = False
