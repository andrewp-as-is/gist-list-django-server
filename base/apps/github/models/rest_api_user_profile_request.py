__all__ = ['RestApiUserProfileRequest']


from django.db import models

class RestApiUserProfileRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    token = models.CharField(max_length=256, null=True)
    priority = models.IntegerField()

    class Meta:
        managed = False
