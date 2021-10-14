from rest_framework import serializers
from friend_request.models import FriendRequest, FriendList
from user.serializers import UserSerializer


class FriendRequestSerializer( serializers.ModelSerializer ):
    status = serializers.CharField( source='get_status_display' )
    request_url = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'sent_date', 'request_url']

    def get_request_url(self, obj):
        url = self.context['request'].build_absolute_uri()
        return f"{url[:-10]}/{obj.id}/"


class FriendListSerializer( serializers.ModelSerializer ):
    class Meta:
        model = FriendList
        fields = ['user', 'friends']

    def to_representation(self, instance):
        representation = super().to_representation( instance )
        representation['user'] = UserSerializer( instance.user, many=False, context=self.context ).data
        return representation
