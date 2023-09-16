__all__ = ['DiscordJob',]

from django.db import models

class DiscordJob(models.Model):
    incident_id = models.IntegerField()

    class Meta:
        managed = False
