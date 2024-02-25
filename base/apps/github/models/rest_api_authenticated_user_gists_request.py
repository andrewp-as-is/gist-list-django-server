__all__ = ['RestApiAuthenticatedUserGistsRequest']


from django.db import models

class RestApiAuthenticatedUserGistsRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    page = models.IntegerField()
    token = models.CharField(max_length=256, null=True)
    priority = models.IntegerField()

    class Meta:
        managed = False
