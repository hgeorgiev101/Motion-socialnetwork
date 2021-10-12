from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import UserSerializer, ProfileSerializer
from rest_framework.response import Response


class ListAllUsersView(ListAPIView):
    """
    get:
    List all users
    search: filter
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        search_string = self.request.query_params.get('search')
        if search_string:
            return User.objects.filter(username__icontains=search_string)
        return User.objects.all()


class ToggleFollowUserView(GenericAPIView):
    """
    post:
    Follow/unfollow users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user not in request.user.following.all() and user != request.user:
            request.user.following.add(user)
        else:
            request.user.following.remove(user)
        return Response(self.get_serializer(user).data)


class ListLoggedInUserFollowedUsers(ListAPIView):
    """
    get:
    List users the currently logged in user is following
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(followers__exact=user)


class ListLoggedInUserFollowers(ListAPIView):
    """
    get:
    List followers of the currently logged in user
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__exact=user)


class SpecificUserView(RetrieveAPIView):
    """
    get:
    Get specific user profile
    """
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'user_id'
