from django.db import models
from user.models import User


def post_directory_path(instance, filename):
    return f'post/{instance.id}/{filename}'


class Post(models.Model):
    text_content = models.CharField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    liked_by = models.ManyToManyField(to=User, related_name='liked_posts', blank=True)
    images = models.ImageField(upload_to=post_directory_path, blank=True, null=True)
    external_link = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'Post ID:{self.id} by {self.author}'


class SharedPost(models.Model):
    parent_post = models.ForeignKey(to=Post, related_name='shared_post', on_delete=models.SET_NULL,
                                    null=True, blank=True)
    child_post = models.ForeignKey(to=Post, related_name='is_shared_by', on_delete=models.SET_NULL, null=True,
                                   blank=True)
