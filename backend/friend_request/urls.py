from django.urls import path

from friend_request.views import ListMyRequests, ListIncomingRequests, SendRequest, GetPatchDeleteRequest, Unfriend

urlpatterns = [
    path('requests/', ListMyRequests.as_view()),
    path('requests/incoming/', ListIncomingRequests.as_view()),
    path('request/<int:receiver_id>/', SendRequest.as_view()),
    path('requests/<int:friend_request_id>/', GetPatchDeleteRequest.as_view()),
    path('unfriend/<int:friend_id>/', Unfriend.as_view())
]
