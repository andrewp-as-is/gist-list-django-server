__all__ = ['GithubUserRefreshLock']

from django.db import models

class GithubUserRefreshLock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('User', related_name='+',on_delete=models.DO_NOTHING)
    github_user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    created_at = models.IntegerField()

    class Meta:
        managed = False
