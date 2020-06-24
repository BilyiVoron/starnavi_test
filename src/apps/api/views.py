from django_filters import rest_framework as rfilters
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.viewsets import GenericViewSet

from apps.api.serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)
from apps.comments.models import Comment
from apps.posts.models import Post


class PostListApiView(GenericViewSet, ListAPIView):
    """
        PostListApiView.
        Users can see all posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "pub_date"]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production


class PostCreateApiView(GenericViewSet, CreateAPIView):
    """
        PostCreateApiView.
        Authorized users can also add new posts
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        PostDetailApiView.
        Authorized users can update or delete their posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)
        return response


class CommentListApiView(GenericViewSet, ListAPIView):
    """
        CommentList.
        Users can see all post's comments
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter, rfilters.DjangoFilterBackend]
    filterset_fields = ("post",)
    ordering_fields = ["post"]
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("pk", None))


class CommentCreateApiView(GenericViewSet, CreateAPIView):
    """
        CommentCreateApiView.
        Authorized users can also add new comments to posts
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, post_id=self.kwargs.get("pk", None))


class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        CommentDetail.
        Authorized users can update or delete their comments
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )  # TODO Delete or comment in production

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)
        return response
