from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from dynamic_rest.serializers import DynamicModelSerializer


from . import models


class FriendSerializer(DynamicModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Friend
        fields = ("id", "name", "has_overdue")
        deferred_fields = ("has_overdue",)


class BelongingSerializer(DynamicModelSerializer):
    class Meta:
        model = models.Belonging
        fields = ("id", "name")


class BorrowedSerializer(DynamicModelSerializer):
    expandable_fields = {
        "what": (BelongingSerializer, {"source": "what"}),
        "to_who": (FriendSerializer, {"source": "to_who"}),
    }

    class Meta:
        model = models.Borrowed
        fields = ("id", "what", "to_who", "when", "returned")
