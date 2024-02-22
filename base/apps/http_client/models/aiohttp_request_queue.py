__all__ = [
    "AiohttpRequestQueue",
]

from django.db import models


class AiohttpRequestQueue(models.Model):
    id = models.AutoField(primary_key=True)
    request_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
