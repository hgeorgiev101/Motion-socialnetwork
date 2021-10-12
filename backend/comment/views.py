from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from comment.models import Comment
from comment.serializers import CommentSerializer
from post.models import Post


class CommentsView(GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_id'
    # permission_classes - default: isAuthenticatedOrReadOnly

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, post=post)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    # api/social/comments/<int:post_id>/ GET: List all comments of a post
