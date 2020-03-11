import django_filters
import pendulum
from django.shortcuts import render
from rest_framework import permissions, viewsets

from . import models, serializers
from .permissions import IsOwner


class FriendViewset(viewsets.ModelViewSet):
    queryset = models.Friend.objects.with_overdue()
    serializer_class = serializers.FriendSerializer
    permission_classes = [IsOwner, permissions.IsAuthenticated]


class BelongingViewset(viewsets.ModelViewSet):
    queryset = models.Belonging.objects.all()
    serializer_class = serializers.BelongingSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class BorrowedFilterSet(django_filters.FilterSet):
    missing = django_filters.BooleanFilter(field_name="returned", lookup_expr="isnull")
    overdue = django_filters.BooleanFilter(method="get_overdue", field_name="returned")

    def get_overdue(
        self, queryset, field_name, value,
    ):
        if value:
            return queryset.filter(when__lte=pendulum.now().subtract(months=2))
        return queryset

    class Meta:
        model = models.Borrowed
        fields = ["what", "to_who", "missing"]


class BorrowedViewset(viewsets.ModelViewSet):
    queryset = models.Borrowed.objects.all()
    serializer_class = serializers.BorrowedSerializer
    permission_classes = [IsOwner]
    filterset_fields = BorrowedFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        only_missing = str(self.request.query_params.get("missing")).lower()
        if only_missing in ["true", "1"]:
            return qs.filter(returned__isnull=True)
        return qs
