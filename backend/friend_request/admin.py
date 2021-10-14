from django.contrib import admin
from friend_request.models import FriendRequest, FriendList


# Register your models here.

class FriendListAdmin( admin.ModelAdmin ):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList


admin.site.register( FriendList, FriendListAdmin )


class FriendRequestAdmin( admin.ModelAdmin ):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__username', 'sender__first_name', 'receiver__username', 'receiver__first_name']

    class Meta:
        model = FriendRequest


admin.site.register( FriendRequest, FriendRequestAdmin )
