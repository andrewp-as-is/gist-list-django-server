__all__ = ['Logout',]

from django.db import models

class Logout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    logout_at = models.FloatField()

    class Meta:
        managed = False
