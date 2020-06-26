from django.urls import path

from apps.api.views import (
    PostListApiView,
    PostCreateApiView,
    PostDetailApiView,
    CommentListApiView,
    CommentCreateApiView,
    CommentDetailApiView,
    LikeUnlikeApiView,
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
        "posts/<int:pk>/like/",
        LikeUnlikeApiView.as_view({"post": "like"}),
        name="post_like",
    ),
    path(
        "posts/<int:pk>/unlike/",
        LikeUnlikeApiView.as_view({"post": "unlike"}),
        name="post_unlike",
    ),
    path(
        "posts/<int:pk>/fans/", LikeUnlikeApiView.as_view({"get": "fans"}), name="post_fans",
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
        "posts/<int:pk>/comments/<int:c_pk>/",
        CommentDetailApiView.as_view(),
        name="comment_detail",
    ),
    path(
        "posts/<int:pk>/comments/<int:c_pk>/like/",
        LikeUnlikeApiView.as_view({"post": "like"}),
        name="comment_like",
    ),
    path(
        "posts/<int:pk>/comments/<int:c_pk>/unlike/",
        LikeUnlikeApiView.as_view({"post": "unlike"}),
        name="comment_unlike",
    ),
    path(
        "posts/<int:pk>/comments/<int:c_pk>/fans/",
        LikeUnlikeApiView.as_view({"get": "fans"}),
        name="comment_fans",
    ),
]
