__all__ = ['UserGraphqlApiFollowingData']

from django.db import models

class UserGraphqlApiFollowingData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    path = models.TextField()
    has_next_page = models.BooleanField()
    processed = models.BooleanField(default=False)

    class Meta:
        managed = False
