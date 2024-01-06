__all__ = ['User',]

# from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django_passwordless_user.models import AbstractBaseUser

class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=39,unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    # django.contrib.admin required
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'

    class Meta:
        managed = False

    def get_absolute_url(self):
        return '/' + self.login

    def get_avatar_url(self):
        return 'https://github.com/%s.png' % (self.login,)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

def user_logged_in_handler(sender, user, request, **kwargs):
    pass


user_logged_in.connect(user_logged_in_handler)
