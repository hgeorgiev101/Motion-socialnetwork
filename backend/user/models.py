from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from project import settings


def user_directory_path(instance, filename):
    return f'user/{instance.id}/{filename}'


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(unique=True)
    following = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='followers', blank=True)
    job = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    banner = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    about_me = models.CharField(max_length=1000, blank=True, null=True)
    things_user_likes = ArrayField(models.CharField(max_length=20), blank=True, null=True, size=10)

    def __str__(self):
        return self.email
