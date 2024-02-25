__all__ = ['GraphqlApiUserGistsRequest']


from django.db import models

class GraphqlApiUserGistsRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    after = models.CharField(max_length=256, null=True)
    token = models.CharField(max_length=256, null=True)
    priority = models.IntegerField()

    class Meta:
        managed = False
