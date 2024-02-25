__all__ = ['ApiRequest']


from django.db import models

class ApiRequest(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField()
    method = models.TextField()
    data = models.TextField(null=True)
    disk_relpath = models.TextField()
    token_id = models.TextField()
    etag = models.TextField(null=True)
    priority = models.IntegerField()

    class Meta:
        managed = False
