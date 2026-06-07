from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializers import TaskSerializer

from .permissions import CanManageTask, IsProjectMember
from activity.utils import log_activity


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated, 
        CanManageTask, 
        IsProjectMember,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "priority",
        "project",
        "assignee",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "priority",
    ]

    ordering = [
        "-created_at"
    ]

    def get_queryset(self):

        user = self.request.user

        return Task.objects.filter(
            project__members=user
        ).select_related(
            "project",
            "assignee",
            "created_by",
        )

    def perform_create(self, serializer):

        task = serializer.save(
            created_by=self.request.user
        )

        log_activity(
            user=self.request.user,
            project=task.project,
            task=task,
            action="Task created"
        )
    
    def perform_update(self, serializer):

        task = serializer.save()

        log_activity(
            user=self.request.user,
            project=task.project,
            task=task,
            action="Task updated"
        )