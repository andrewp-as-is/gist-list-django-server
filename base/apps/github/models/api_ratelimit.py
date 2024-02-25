__all__ = ['ApiRatelimit']


from django.db import models

class ApiRatelimit(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.TextField()
    resource = models.TextField() # core, graphql, search
    remaining = models.IntegerField()
    reset = models.IntegerField()

    class Meta:
        managed = False
