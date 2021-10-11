from rest_framework import serializers

from post.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked_by_me = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked_by_me(self, obj):
        if self.context['request'].user not in obj.liked_by.all():
            return False
        else:
            return True

    class Meta:
        model = Post
        fields = ['id', 'text_content', 'created', 'author', 'like_count', 'is_liked_by_me', 'images', 'external_link']
        read_only_fields = ['author']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author, many=False, context=self.context).data
        return representation
