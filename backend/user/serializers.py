from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User
from post.models import Post


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_of_count = serializers.SerializerMethodField()
    is_followed_by_me = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_posts_of_count(self, user):
        return Post.objects.filter(author=user).count()

    def get_is_followed_by_me(self, obj):
        request = self.context.get('request', None)
        if request:
            if self.context['request'].user not in obj.followers.all():
                return False
            else:
                return True

    def get_avatar_url(self, obj):
        try:
            domain_name = 'https://motion-team-php.propulsion-learn.ch'
            full_path = domain_name + obj.avatar.url
            return full_path
        except:
            return None

    class Meta:
        model = User
        fields = ['is_followed_by_me', 'id', 'username', 'first_name', 'last_name', 'email',
                  'job', 'avatar', 'banner', 'location', 'about_me',
                  'things_user_likes', 'followers_count', 'following_count', 'posts_of_count', 'avatar_url']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avatar'] = representation.pop('avatar_url')
        return representation


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_of_count = serializers.SerializerMethodField()
    is_followed_by_me = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_posts_of_count(self, user):
        return Post.objects.filter(author=user).count()

    def get_is_followed_by_me(self, obj):
        request = self.context.get('request', None)
        if request:
            if self.context['request'].user not in obj.followers.all():
                return False
            else:
                return True

    def get_avatar_url(self, obj):
        try:
            domain_name = 'https://motion-team-php.propulsion-learn.ch'
            full_path = domain_name + obj.avatar.url
            return full_path
        except:
            return None
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'following', 'followers', 'job', 'avatar',
                  'banner', 'location', 'about_me',
                  'things_user_likes', 'followers_count', 'following_count', 'posts_of_count', 'is_followed_by_me',
                  'avatar_url']
        # read_only_fields = []

    # need to add "is friends", "is rejected", "received FR", "sent FR", "# friends"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avatar'] = representation.pop('avatar_url')
        return representation


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user': ProfileSerializer(self.user, many=False).data})
        return data
