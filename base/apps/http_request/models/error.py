__all__ = ['Error',]


from django.db import models

class Error(models.Model):
    domain = models.TextField()
    url = models.TextField()
    exc_type = models.TextField()
    timestamp = models.IntegerField()
