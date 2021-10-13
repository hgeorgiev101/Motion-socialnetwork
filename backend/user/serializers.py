from rest_framework import serializers

from user.models import User
from post.models import Post


class UserSerializer(serializers.ModelSerializer):
    is_followed_by_me = serializers.SerializerMethodField()

    def get_is_followed_by_me(self, obj):
        if self.context['request'].user not in obj.followers.all():
            return False
        else:
            return True

    class Meta:
        model = User
        fields = ['id', 'username', 'is_followed_by_me']


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_of_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_posts_of_count(self, user):
        return Post.objects.filter(author=user).count()

    class Meta:
        model = User
        fields = ['id', 'email', 'following', 'followers', 'job', 'avatar', 'banner', 'location', 'about_me',
                  'things_user_likes', 'followers_count', 'following_count', 'posts_of_count']
        # read_only_fields = []
#need to add "is friends", "is rejected", "received FR", "sent FR", "# friends"