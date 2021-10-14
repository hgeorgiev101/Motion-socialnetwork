from django.db import models

from post.models import Post
from user.models import User


class Comment(models.Model):
    content = models.CharField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    # liked_by = models.ManyToManyField(to=User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f'Comment ID:{self.id} by {self.author}'
