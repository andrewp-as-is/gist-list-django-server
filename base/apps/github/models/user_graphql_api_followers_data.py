__all__ = ['UserGraphqlApiFollowersData']

from django.db import models

class UserGraphqlApiFollowersData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    path = models.TextField()
    has_next_page = models.BooleanField()
    processed = models.BooleanField(default=False)

    class Meta:
        managed = False
