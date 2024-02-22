__all__ = ['AbstractFollowing','Following']

from django.db import models

class AbstractFollowing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    following = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    row_number_over_login = models.IntegerField(null=True)
    row_number_over_name = models.IntegerField(null=True)
    row_number_over_followers = models.IntegerField(null=True)
    row_number_over_following = models.IntegerField(null=True)
    row_number_over_gists = models.IntegerField(null=True)

    class Meta:
        abstract = True

class Following(AbstractFollowing):
   # user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    #following = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        unique_together = ('user', 'following',)
