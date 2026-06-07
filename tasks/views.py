from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return Task.objects.filter(
            project__members=user
        ).select_related(
            "project",
            "assignee",
            "created_by"
        )

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )