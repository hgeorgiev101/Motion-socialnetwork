from rest_framework import serializers

from user.models import User


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
