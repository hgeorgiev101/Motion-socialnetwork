from django.urls import path

from user.views import ToggleFollowUserView, ListLoggedInUserFollowedUsers, ListLoggedInUserFollowers

urlpatterns = [
    path('toggle-follow/<int:user_id>/', ToggleFollowUserView.as_view()),
    path('following/', ListLoggedInUserFollowedUsers.as_view()),
    path('followers/', ListLoggedInUserFollowers.as_view())
]
