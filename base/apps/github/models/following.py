__all__ = ['Following']

from django.db import models

class Following(models.Model):

    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    following = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = ('user', 'following',)
