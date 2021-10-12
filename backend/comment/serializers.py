from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created', 'updated', 'post', 'author'] # deleted author here. should be automatic
        read_only_fields = ['author', 'post']