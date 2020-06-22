from django.urls import path

from apps.api.views import (
    PostListApiView,
    PostCreateApiView,
    PostDetailApiView,
    CommentListApiView,
    CommentCreateApiView,
    CommentDetailApiView,
    # UserReactionApiView,
)
from apps.api.viewsets import PostViewSet

app_name = "api"

urlpatterns = [
    path("posts/", PostListApiView.as_view({"get": "list"}), name="posts_list"),
    path("post_url/", PostViewSet),
    path(
        "post_create/",
        PostCreateApiView.as_view({"post": "create"}),
        name="create_list",
    ),
    path("posts/<int:pk>/", PostDetailApiView.as_view(), name="post_detail"),
    path(
        "comments/", CommentListApiView.as_view({"get": "list"}), name="comments_list"
    ),
    path(
        "comment_create/",
        CommentCreateApiView.as_view({"post": "create"}),
        name="comment_create",
    ),
    path("comments/<int:pk>/", CommentDetailApiView.as_view(), name="comment_detail"),
    # path(
    #     "posts/<int:pk>/like_unlike/",
    #     UserReactionApiView.as_view({"post": "update"}),
    #     name="post_like_unlike",
    # ),
    # path(
    #     "comments/<int:pk>/like_unlike/",
    #     UserReactionApiView.as_view({"post": "update"}),
    #     name="comment_like_unlike",
    # ),
]
