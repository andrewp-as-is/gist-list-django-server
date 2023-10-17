__all__ = ['DiscordWebhook',]

from django.db import models

class DiscordWebhook(models.Model):
    url = models.CharField(unique=True,max_length=255)

    class Meta:
        managed = False
        ordering = ('url', )
