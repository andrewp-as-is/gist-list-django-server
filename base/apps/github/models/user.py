__all__ = ['AbstractUser','User',]

from django.contrib.postgres.fields import ArrayField
from django.db import models

"""
https://developer.github.com/v3/users/
"""

class AbstractUser(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=39,unique=True)
    type = models.CharField(max_length=100)
    name = models.TextField(null=True)
    company = models.TextField(null=True)
    blog = models.TextField(null=True)
    location = models.TextField(null=True)
    bio = models.TextField(null=True,blank=True)
    email = models.TextField(null=True)
    twitter_username = models.TextField(null=True)

    followers_count = models.IntegerField(null=True)
    following_count = models.IntegerField(null=True)

    public_gists_count = models.IntegerField(null=True)
    private_gists_count = models.IntegerField(null=True)
    stars_count = models.IntegerField(null=True)
    public_forks_count = models.IntegerField(null=True)
    private_forks_count = models.IntegerField(null=True)

    created_at = models.IntegerField(null=True)
    updated_at = models.IntegerField(null=True)

    # CUSTOM FIELDS
    language_list = ArrayField(models.TextField()) # language NAME list
    tag_list = ArrayField(models.TextField()) # tag SLUG list

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/' + self.login

    def get_avatar_url(self):
        return 'https://github.com/%s.png' % (self.login,)

class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
