__all__ = ['AbstractAuthenticatedUserStat','AuthenticatedUserStat',]

from django.db import models

from django.contrib.postgres.fields import ArrayField

class AbstractAuthenticatedUserStat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)

    gists_count = models.IntegerField(null=True)
    forks_count = models.IntegerField(null=True)
    stars_count = models.IntegerField(null=True)
    files_count = models.IntegerField(null=True)
    trash_count = models.IntegerField(null=True)

    language_stat = models.TextField(null=True)
    tag_stat = models.TextField(null=True)
    type_stat = models.TextField(null=True)

    gists_refreshed_at = models.IntegerField(null=True)
    starred_gists_refreshed_at = models.IntegerField(null=True)
    locked_at = models.IntegerField(null=True)
    refreshed_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

class AuthenticatedUserStat(AbstractAuthenticatedUserStat):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
