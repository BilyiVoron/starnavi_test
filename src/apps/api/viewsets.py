from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.api.mixins import LikedMixin
from apps.api.serializers import PostSerializer, CommentSerializer
from apps.comments.models import Comment
from apps.posts.models import Post


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        print(Post.objects.filter(id=self.kwargs.get("pk", None)))
        return Post.objects.filter(id=self.kwargs.get("pk", None))


class CommentViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs.get("p_pk", None))

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("p_pk", None))
