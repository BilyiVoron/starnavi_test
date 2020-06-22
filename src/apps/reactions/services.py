from django.contrib.contenttypes.models import ContentType

from apps.reactions.models import Like, Unlike
from apps.users.models import User


# def add_like_or_unlike(obj, owner, likes: bool, unlikes: bool):
def add_like(obj, owner):
    """
    Likes "obj".
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, owner=owner)
    return like


# def remove_like_or_unlike(obj, owner, likes: bool, unlikes: bool):
def remove_like(obj, owner):
    """
    Remove like from "obj".
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, owner=owner).delete()


# def is_fan_or_hater(obj, owner, likes, unlikes) -> bool:
def is_fan(obj, owner) -> bool:
    """
    Check if user likes "obj".
    """
    if not owner.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, owner=owner)
    return likes.exists()



# def get_fans_or_haters(obj, likes: bool, unlikes: bool):
def get_fans(obj):
    """
    Get all users which have liked "obj".
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)


def add_unlike(obj, owner):
    """
    Unlikes "obj".
    """
    obj_type = ContentType.objects.get_for_model(obj)
    unlike, is_created = Unlike.objects.get_or_create(content_type=obj_type, object_id=obj.id, owner=owner)
    return unlike


def remove_unlike(obj, owner):
    """
    Remove unlike from "obj".
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Unlike.objects.filter(content_type=obj_type, object_id=obj.id, owner=owner).delete()


def is_hater(obj, owner) -> bool:
    """
    Check if user unlikes "obj".
    """
    if not owner.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    unlikes = Unlike.objects.filter(content_type=obj_type, object_id=obj.id, owner=owner)
    return unlikes.exists()


def get_haters(obj):
    """
    Get all users which have unliked "obj".
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(unlikes__content_type=obj_type, unlikes__object_id=obj.id)
