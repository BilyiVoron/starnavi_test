from django_filters import rest_framework as rfilters
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.comments.models import Comment, CommentUserReaction
from apps.comments.serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentUserReactionSerializer,
)
from apps.posts.models import Post, PostUserReaction
from apps.posts.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostUserReactionSerializer,
)


def update_reaction_post(obj_base: PostUserReaction, obj: PostUserReaction, like: bool, unlike: bool):
    """
        Realized Like/Unlike system.
        User can vote only once:
        "Like" or "Unlike".
    """
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


def update_reaction_comment(obj_base: CommentUserReaction, obj: CommentUserReaction, like: bool, unlike: bool):
    """
        Realized Like/Unlike system.
        User can vote only once:
        "Like" or "Unlike".
    """
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
        PostListApiView.
        Users can see all posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "pub_date", "like"]


class PostCreateApiView(GenericViewSet, CreateAPIView):
    """
        PostCreateApiView.
        Authorized users can also add new posts
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        PostDetailApiView.
        Authorized users can update or delete their posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

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


class CommentCreateApiView(GenericViewSet, CreateAPIView):
    """
        CommentCreateApiView.
        Authorized users can also add new comments to posts
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        CommentDetail.
        Authorized users can update or delete their comments
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)
        return response


class PostUserReactionApiView(GenericViewSet, UpdateModelMixin):
    """
        PostLikeUnlikeApiView.
        Authorized users can vote posts by "Like" or "Unlike" buttons
    """

    queryset = Post.objects.all()
    serializer_class = PostUserReactionSerializer

    @staticmethod
    def create_update_reaction(post: PostUserReaction, owner_id: int, like: bool, unlike: bool):
        try:
            post_reaction = PostUserReaction.objects.get(post=post, owner_id=owner_id)
            post_reaction = update_reaction_post(
                obj_base=post, obj=post_reaction, like=like, unlike=unlike
            )
        except PostUserReaction.DoesNotExist:
            post_reaction = PostUserReaction()
            post_reaction.post = post
            post_reaction.owner_id = owner_id
            post_reaction = update_reaction_post(
                obj_base=post, obj=post_reaction, like=like, unlike=unlike
            )
        return post_reaction

    def reaction(self, request, post):
        owner_id = request.data.get("owner", None)
        like = request.data.get("like", False)
        unlike = request.data.get("unlike", False)
        post_reaction = self.create_update_reaction(
            post=post, owner_id=owner_id, like=like, unlike=unlike
        )
        return post_reaction

    def get_object(self):
        return self.queryset

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get("pk", None))

            request.data["owner"] = request.user.id
            self.queryset = self.reaction(request, post)
            request.data.update(dict(self.serializer_class(self.queryset).data))
            response = super().update(request, *args, **kwargs)
            return response
        except Post.DoesNotExist:
            return Response(data={"detail": "Not found"}, status=500)


class CommentUserReactionApiView(GenericViewSet, UpdateModelMixin):
    """
        CommentLikeUnlikeApiView.
        Authorized users can vote comments by "Like" or "Unlike" buttons
    """

    queryset = Comment.objects.all()
    serializer_class = CommentUserReactionSerializer

    @staticmethod
    def create_update_reaction(
        comment: CommentUserReaction, owner_id: int, like: bool, unlike: bool
    ):
        try:
            comment_reaction = CommentUserReaction.objects.get(
                comment=comment, owner_id=owner_id
            )
            comment_reaction = update_reaction_comment(
                obj_base=comment, obj=comment_reaction, like=like, unlike=unlike
            )
        except CommentUserReaction.DoesNotExist:
            comment_reaction = CommentUserReaction()
            comment_reaction.comment = comment
            comment_reaction.owner_id = owner_id
            comment_reaction = update_reaction_comment(
                obj_base=comment, obj=comment_reaction, like=like, unlike=unlike
            )
        return comment_reaction

    def reaction(self, request, comment):
        owner_id = request.data.get("owner", None)
        like = request.data.get("like", False)
        unlike = request.data.get("unlike", False)
        comment_reaction = self.create_update_reaction(
            comment=comment, owner_id=owner_id, like=like, unlike=unlike
        )
        return comment_reaction

    def get_object(self):
        return self.queryset

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs.get("pk", None))
            request.data["owner"] = request.user.id
            self.queryset = self.reaction(request, comment)
            request.data.update(dict(self.serializer_class(self.queryset).data))
            response = super().update(request, *args, **kwargs)
            return response
        except Comment.DoesNotExist:
            return Response(data={"detail": "Not found"}, status=500)
