__all__ = ['Cursor',]

from django.db import models

class Cursor(models.Model):
    schemaname = models.CharField(max_length=255)
    viewname = models.CharField(max_length=255)
    job_id = models.IntegerField()
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-created_at', )
        unique_together = [('schemaname', 'viewname',)]

