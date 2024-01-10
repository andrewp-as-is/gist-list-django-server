__all__ = ['UserTableModification',]

from django.db import models

class UserTableModification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    tablename = models.FloatField()
    modified_at = models.FloatField()

    class Meta:
        managed = False
        unique_together = [('user', 'tablename',)]
