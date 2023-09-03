__all__ = ['AbstractUser','User','UserBase']

from django.db import models

from base.utils import execute_sql

"""
https://developer.github.com/v3/users/
"""

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['id'],
                update_fields = [
                    'login',
                    'type',
                    'name',
                    'company',
                    'blog',
                    'location',
                    'bio',
                    'email',
                    'twitter_username',
                    'public_gists_count',
                    'followers_count',
                    'following_count',
                    'created_at',
                    'updated_at'
                ]
            )
        try:
            return super().bulk_create(objs,**kwargs)
        finally:
            execute_sql('VACUUM FULL github."user"')

class AbstractUser(models.Model):
    objects = Manager()

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

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/' + self.login

    def get_avatar_url(self):
        return 'https://github.com/%s.png' % (self.login,)

class User(AbstractUser):
    objects = Manager()

    class Meta:
        managed = False


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['id'],
                update_fields = [
                    'login',
                ]
            )
        return super().bulk_create(objs,**kwargs)

class UserBase(models.Model):
    objects = Manager()

    login = models.CharField(max_length=39,unique=True)

    class Meta:
        managed = False