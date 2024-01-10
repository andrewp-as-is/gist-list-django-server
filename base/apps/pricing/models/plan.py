__all__ = ['Plan',]

from django.db import models

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True,max_length=255)
    order = models.IntegerField(unique=True)

    class Meta:
        managed = False
        ordering = ('order', )
