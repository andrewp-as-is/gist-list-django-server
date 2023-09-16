__all__ = ['Following']

from django.db import models

from base.apps.github_matview.models import AbstractFollowing

class Following(AbstractFollowing):
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.CASCADE)
    following = models.ForeignKey('User', related_name='+',on_delete=models.CASCADE)

    class Meta:
        managed = False
        unique_together = [('user', 'following',)]
