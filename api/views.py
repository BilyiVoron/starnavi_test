from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin

from starnaviapp.models import Post, Comment
from starnaviapp.permissions import IsPostOwnerOrAdmin, IsCommentOwnerOrAdmin
from starnaviapp.serializers import PostSerializer, CommentSerializer


class PostList(ViewSetMixin, generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostOwnerOrAdmin, IsAuthenticated)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "pub_date", "like"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostOwnerOrAdmin, IsAuthenticated)


class CommentList(ViewSetMixin, generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsCommentOwnerOrAdmin, IsAuthenticated)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["post"]

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs.get("p_pk", None))

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.kwargs.get("p_pk", None))
        return queryset


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsCommentOwnerOrAdmin, IsAuthenticated)
