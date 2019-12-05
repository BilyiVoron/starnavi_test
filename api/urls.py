from django.urls import path

from api.views import PostList, PostDetail, CommentList, CommentDetail

app_name = "api"

urlpatterns = [
    path("posts/", PostList.as_view({"get": "list"}), name="posts"),
    path("posts/<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("posts/<int:p_pk>/comments/", CommentList.as_view({"get": "list"}), name="comments",),
    path("posts/<int:p_pk>/comments/<int:pk>/", CommentDetail.as_view(), name="comment_detail",),
]
