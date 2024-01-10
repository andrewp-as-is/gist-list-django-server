__all__ = ['Following']

from django.db import models

from base.apps.github_matview.models import AbstractFollowing

class Following(AbstractFollowing):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    following = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = [('user', 'following',)]
