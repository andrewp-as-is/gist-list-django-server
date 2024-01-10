__all__ = ['Login',]

from django.db import models

class Login(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    login_at = models.FloatField()

    class Meta:
        managed = False
