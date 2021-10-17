from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friend_request.models import FriendList
from post.models import Post
from post.permissions import IsOwnerOrAdminOrReadOnly
from post.serializers import PostSerializer


class ListCreatePostsView(ListCreateAPIView):
    """
    get:
    List all posts. No authorization needed
    post:
    Create a new post.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created')
        search_string = self.request.query_params.get( 'search' )
        if search_string:
            queryset = queryset.filter(
                Q(text_content__icontains=search_string) | Q(external_link__icontains=search_string))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, liked_by='')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):
    """
    get:
    List a post by id
    patch:
    Update a post by id. Only the author or an admin can perform this action.
    delete:
    Delete a post by id. Only the author or an admin can perform this action.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'
    permission_classes = [IsOwnerOrAdminOrReadOnly]


class ToggleLikePostView(GenericAPIView):
    """
    post:
    Like/unlike a post by id.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
        else:
            post.liked_by.remove(request.user)
        return Response(self.get_serializer(post).data)


class ListLikedPostsByCurrentUserView(ListAPIView):
    """
    get:
    List all liked posts of the currently logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return Post.objects.filter(liked_by__exact=user)


class ListCurrentUserPostsOfFollowingView(ListAPIView):
    """
    get:
    List all posts of the users the currently logged in user is following.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return Post.objects.filter(author__in=user.following.all())


class ListPostsByUserIdView(ListAPIView):
    """
    get:
    List all posts made by a user.
    """
    serializer_class = PostSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        user = self.kwargs.get('user_id')
        return Post.objects.filter(author_id__exact=user).order_by('-created')


class PostsByFriends(GenericAPIView):
    """
    get:
    List all posts made by friends of current user.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            friends_list = FriendList.objects.get(user=user)
            queryset = self.get_queryset()
            queryset = queryset.filter(author__in=friends_list.friends.all())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response('No friends found!', status=status.HTTP_204_NO_CONTENT)
