__all__ = ['AbstractUserStat','UserStat',]

from django.db import models

from django.contrib.postgres.fields import ArrayField

class AbstractUserStat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)

    public_gists_count = models.IntegerField(null=True)
    secret_gists_count = models.IntegerField(null=True)

    public_forks_count = models.IntegerField(null=True)
    secret_forks_count = models.IntegerField(null=True)

    stars_count = models.IntegerField(null=True)
    trash_count = models.IntegerField(null=True)

    public_language_stat = models.TextField(null=True)
    secret_language_stat = models.TextField(null=True)
    public_tag_stat = models.TextField(null=True)
    secret_tag_stat = models.TextField(null=True)
    starred_language_stat = models.TextField(null=True)
    starred_tag_stat = models.TextField(null=True)

   # public_language_list = ArrayField(models.TextField()) # language NAME list
   # public_tag_list = ArrayField(models.TextField()) # tag SLUG list

    refreshed_at = models.IntegerField(null=True)
    secret_refreshed_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

class UserStat(AbstractUserStat):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
