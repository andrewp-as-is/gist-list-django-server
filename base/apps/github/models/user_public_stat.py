__all__ = ['AbstractUserPublicStat','UserPublicStat',]

from django.db import models

from django.contrib.postgres.fields import ArrayField

class AbstractUserPublicStat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)

    gists_count = models.IntegerField(null=True)
    forks_count = models.IntegerField(null=True)
    # stars_count = models.IntegerField(null=True) SECRET ONLY
    files_count = models.IntegerField(null=True)
    # trash_count = models.IntegerField(null=True) SECRET ONLY

    language_stat = models.TextField(null=True)
    tag_stat = models.TextField(null=True)
    type_stat = models.TextField(null=True)

    locked_at = models.IntegerField(null=True)
    refreshed_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

class UserPublicStat(AbstractUserPublicStat):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
