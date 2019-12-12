from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from starnaviapp.models import Post, Comment, PostLikeUnlike, CommentLikeUnlike
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from starnaviapp.serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    PostLikeUnlikeSerializer,
    CommentLikeUnlikeSerializer,
)


User = get_user_model()


def update_like_unlike_obj(obj_base: object, obj: object, like: bool, unlike: bool):
    if like and not unlike:
        if obj.like:
            obj_base.like -= 1
            obj.like = False
            obj.unlike = False
        else:
            obj_base.like += 1
            obj.like = True
            obj.unlike = False
    elif unlike and not like:
        if obj.unlike:
            obj_base.unlike -= 1
            obj.like = False
            obj.unlike = False
        else:
            obj_base.unlike += 1
            obj.like = False
            obj.unlike = True
    obj_base.save()
    obj.save()
    return obj


class PostListApiView(GenericViewSet, ListAPIView):
    """
        PostListApiView
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "pub_date", "like"]


class PostCreateApiView(GenericViewSet, CreateAPIView):
    """
        PostCreateApiView
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        PostDetailApiView
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ["get", "put", "delete"]

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)
        return response


class CommentListApiView(GenericViewSet, ListAPIView):
    """
        CommentList
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["post"]


class CommentCreateApiView(GenericViewSet, CreateAPIView):
    """
        CommentCreateApiView
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        CommentDetail
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ["get", "put", "delete"]

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)
        return response


class PostLikeUnlikeApiView(GenericViewSet, UpdateModelMixin):
    """
        PostLikeUnlikeApiView
    """

    queryset = Post.objects.all()
    serializer_class = PostLikeUnlikeSerializer

    @staticmethod
    def create_update_like_unlike(post: Post, owner_id: int, like: bool, unlike: bool):
        try:
            post_like_unlike = PostLikeUnlike.objects.get(post=post, owner_id=owner_id)
            post_like_unlike = update_like_unlike_obj(
                obj_base=post, obj=post_like_unlike, like=like, unlike=unlike
            )
        except PostLikeUnlike.DoesNotExist:
            post_like_unlike = PostLikeUnlike()
            post_like_unlike.post = post
            post_like_unlike.owner_id = owner_id
            post_like_unlike = update_like_unlike_obj(
                obj_base=post, obj=post_like_unlike, like=like, unlike=unlike
            )
        return post_like_unlike

    def like_unlike(self, request, post):
        owner_id = request.data.get("owner", None)
        like = request.data.get("like", False)
        unlike = request.data.get("unlike", False)
        post_like_unlike = self.create_update_like_unlike(
            post=post, owner_id=owner_id, like=like, unlike=unlike
        )
        return post_like_unlike

    def get_object(self):
        return self.queryset

    def update(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get("pk", None))
            request.data["owner"] = request.user.id
            self.queryset = self.like_unlike(request, post)
            request.data.update(dict(self.serializer_class(self.queryset).data))
            response = super().update(request, *args, **kwargs)
            return response
        except Post.DoesNotExist:
            return Response(data={"detail": "Not found"}, status=500)


class CommentLikeUnlikeApiView(GenericViewSet, UpdateModelMixin):
    """
        CommentLikeUnlikeApiView
    """

    queryset = Comment.objects.all()
    serializer_class = CommentLikeUnlikeSerializer

    @staticmethod
    def create_update_like_unlike(
        comment: Comment, owner_id: int, like: bool, unlike: bool
    ):
        try:
            comment_like_unlike = CommentLikeUnlike.objects.get(
                comment=comment, owner_id=owner_id
            )
            comment_like_unlike = update_like_unlike_obj(
                obj_base=comment, obj=comment_like_unlike, like=like, unlike=unlike
            )
        except CommentLikeUnlike.DoesNotExist:
            comment_like_unlike = CommentLikeUnlike()
            comment_like_unlike.comment = comment
            comment_like_unlike.owner_id = owner_id
            comment_like_unlike = update_like_unlike_obj(
                obj_base=comment, obj=comment_like_unlike, like=like, unlike=unlike
            )
        return comment_like_unlike

    def like_unlike(self, request, comment):
        owner_id = request.data.get("owner", None)
        like = request.data.get("like", False)
        unlike = request.data.get("unlike", False)
        comment_like_unlike = self.create_update_like_unlike(
            comment=comment, owner_id=owner_id, like=like, unlike=unlike
        )
        return comment_like_unlike

    def get_object(self):
        return self.queryset

    def update(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs.get("pk", None))
            request.data["owner"] = request.user.id
            self.queryset = self.like_unlike(request, comment)
            request.data.update(dict(self.serializer_class(self.queryset).data))
            response = super().update(request, *args, **kwargs)
            return response
        except Comment.DoesNotExist:
            return Response(data={"detail": "Not found"}, status=500)
