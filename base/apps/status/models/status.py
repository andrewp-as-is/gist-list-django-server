__all__ = ['Status',]

from django.db import models

class Status(models.Model):
    healthcheck_success = models.BooleanField()
    incidents_count = models.IntegerField()
    created_at = models.IntegerField()

    class Meta:
        managed = False

    @property
    def success(self):
        return self.healthcheck_success and self.incidents_count==0
