__all__ = [
    "AiohttpRequestPush",
]

from django.db import models


class AiohttpRequestPush(models.Model):
    id = models.AutoField(primary_key=True)
    request_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
