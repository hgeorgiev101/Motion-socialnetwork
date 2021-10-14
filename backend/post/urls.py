from django.urls import path

from post.views import ListCreatePostsView, RetrieveUpdateDeletePostView, ToggleLikePostView, \
    ListLikedPostsByCurrentUserView, ListPostsByUserIdView, ListCurrentUserPostsOfFollowingView, PostsByFriends


urlpatterns = [
    path('', ListCreatePostsView.as_view()),
    path('<int:post_id>/', RetrieveUpdateDeletePostView.as_view()),
    path('toggle-like/<int:post_id>/', ToggleLikePostView.as_view()),
    path('likes/', ListLikedPostsByCurrentUserView.as_view()),
    path('following/', ListCurrentUserPostsOfFollowingView.as_view()),
    path('user/<int:user_id>/', ListPostsByUserIdView.as_view()),
    path('friends/', PostsByFriends.as_view()),
]
