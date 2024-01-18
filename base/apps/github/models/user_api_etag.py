__all__ = ['UserApiEtag']

from django.db import models

class UserApiEtag(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    url = models.CharField(max_length=255,unique=True)
    etag = models.CharField(max_length=255)

    class Meta:
        managed = False
