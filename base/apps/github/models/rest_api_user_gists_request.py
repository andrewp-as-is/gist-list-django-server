__all__ = ['RestApiUserGistsRequest']


from django.db import models

class RestApiUserGistsRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    page = models.IntegerField()
    token = models.CharField(max_length=256, null=True)
    priority = models.IntegerField()

    class Meta:
        managed = False
