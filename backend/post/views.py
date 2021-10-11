from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.all().order_by('-created')


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
