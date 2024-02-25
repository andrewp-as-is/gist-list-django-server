__all__ = ['GithubRequestLimit']

from django.db import models

class GithubRequestLimit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
