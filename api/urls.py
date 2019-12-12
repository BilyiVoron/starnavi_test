from django.urls import path
from api.views import (
    PostListApiView,
    PostCreateApiView,
    PostDetailApiView,
    CommentListApiView,
    CommentCreateApiView,
    CommentDetailApiView,
    PostLikeUnlikeApiView,
    CommentLikeUnlikeApiView,
)


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
        "comments/", CommentListApiView.as_view({"get": "list"}), name="comments_list"
    ),
    path(
        "comment_create/",
        CommentCreateApiView.as_view({"post": "create"}),
        name="comment_create",
    ),
    path("comments/<int:pk>/", CommentDetailApiView.as_view(), name="comment_detail"),
    path(
        "post_like_unlike/<int:pk>/",
        PostLikeUnlikeApiView.as_view({"post": "update"}),
        name="post_like_unlike",
    ),
    path(
        "comment_like_unlike/<int:pk>/",
        CommentLikeUnlikeApiView.as_view({"post": "update"}),
        name="comment_like_unlike",
    ),
]
