__all__ = ['MatviewTime']

from django.db import models

class MatviewTime(models.Model):
    user = models.ForeignKey('github.User', related_name='+',on_delete=models.DO_NOTHING)
    follower_expired_at = models.IntegerField(null=True)
    following_expired_at = models.IntegerField(null=True)
    gist_expired_at = models.IntegerField(null=True)
    gist_language_expired_at = models.IntegerField(null=True)
    gist_tag_expired_at = models.IntegerField(null=True)
    user_expired_at = models.IntegerField(null=True)

    class Meta:
        managed = False
