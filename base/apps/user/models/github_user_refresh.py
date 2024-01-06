__all__ = ['GithubUserRefresh']

from django.db import models

class GithubUserRefresh(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField('User', related_name='+',on_delete=models.DO_NOTHING)
    github_user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    started_at = models.IntegerField()
    finished_at = models.IntegerField(null=True)

    class Meta:
        managed = False
