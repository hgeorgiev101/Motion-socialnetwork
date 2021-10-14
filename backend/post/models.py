from django.db import models
from user.models import User


def post_directory_path(instance, filename):
    return f'post/{instance.author.id}/{filename}'


class Post(models.Model):
    text_content = models.CharField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    liked_by = models.ManyToManyField(to=User, related_name='liked_posts', blank=True)
    images = models.ImageField(upload_to=post_directory_path, blank=True, null=True)
    external_link = models.CharField(max_length=500, blank=True, null=True)
    shared_post = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='parent')

    @property
    def is_parent(self):
        if self.shared_post is None:
            return False
        return True

    def __str__(self):
        return f'Post ID:{self.id} by {self.author}'
