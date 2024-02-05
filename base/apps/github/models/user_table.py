__all__ = ['AbstractUserTable','UserTable',]

from django.db import models

from django.contrib.postgres.fields import ArrayField

class AbstractUserTable(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)

    gist_modified_at = models.IntegerField(null=True)
    gist_star_modified_at = models.IntegerField(null=True)
    user_follower_modified_at = models.IntegerField(null=True)
    user_following_modified_at = models.IntegerField(null=True)
    user_modified_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

class UserTable(AbstractUserTable):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
