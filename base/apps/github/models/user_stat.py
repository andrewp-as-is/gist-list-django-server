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
    gist_trash_count = models.IntegerField(null=True)

    language_list = ArrayField(models.TextField()) # language NAME list
    tag_list = ArrayField(models.TextField()) # tag SLUG list

    class Meta:
        abstract = True

class UserStat(AbstractUserStat):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
