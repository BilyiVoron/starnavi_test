from django.urls import path

from apps.api.mixins import LikedMixin
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
    path(
        "posts/<int:pk>/like/",
        PostViewSet.as_view({"post": "like"}),
        name="like",
    ),
    path(
        "posts/<int:pk>/comments/",
        CommentListApiView.as_view({"get": "list"}),
        name="comments_list",
    ),
    path(
        "posts/<int:pk>/comment_create/",
        CommentCreateApiView.as_view({"post": "create"}),
        name="comment_create",
    ),
    path(
        "posts/<int:p_pk>/comments/<int:pk>/",
        CommentDetailApiView.as_view(),
        name="comment_detail",
    ),
    path(
        "posts/<int:p_pk>/comments/<int:pk>/reactions/",
        CommentViewSet.as_view({"get": "list"}),
        name="comment_reactions",
    ),
]
