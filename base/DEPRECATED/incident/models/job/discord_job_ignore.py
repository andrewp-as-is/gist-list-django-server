__all__ = ['DiscordJobIgnore',]

from django.db import models

class DiscordJobIgnore(models.Model):
    incident_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
