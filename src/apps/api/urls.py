from django.urls import path

from apps.api.views import (
    PostListApiView,
    PostCreateApiView,
    PostDetailApiView,
    CommentListApiView,
    CommentCreateApiView,
    CommentDetailApiView,
)
from apps.api.viewsets import PostViewSet, CommentViewSet

app_name = "api"

urlpatterns = [
    path("posts/", PostListApiView.as_view({"get": "list"}), name="posts_list"),
    path(
        "post_create/",
        PostCreateApiView.as_view({"post": "create"}),
        name="create_list",
    ),
    path("posts/<int:pk>/", PostDetailApiView.as_view(), name="post_detail"),
    path("posts/<int:pk>/reactions/", PostViewSet.as_view({"get": "list"}), name="post_reactions"),
    path(
        "comments/", CommentListApiView.as_view({"get": "list"}), name="comments_list"
    ),
    path(
        "comment_create/",
        CommentCreateApiView.as_view({"post": "create"}),
        name="comment_create",
    ),
    path("comments/<int:pk>/", CommentDetailApiView.as_view(), name="comment_detail"),
    path("comments/<int:pk>/reactions/", CommentViewSet.as_view({"get": "list"}), name="comment_reactions"),
]
