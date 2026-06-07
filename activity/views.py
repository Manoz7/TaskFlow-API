from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import ActivityLog
from .serializers import ActivityLogSerializer


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ActivityLogSerializer

    permission_classes = [
        IsAuthenticated
    ]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "project",
        "task",
        "user",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at"
    ]

    def get_queryset(self):

        return ActivityLog.objects.filter(
            project__members=self.request.user
        ).select_related(
            "user",
            "project",
            "task"
        ).distinct()