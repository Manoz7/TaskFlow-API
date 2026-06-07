from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwnerOrAdminManager

from activity.utils import log_activity
from rest_framework.exceptions import PermissionDenied



class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated,
        IsCommentOwnerOrAdminManager,
    ]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "task",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):

        user = self.request.user

        return Comment.objects.filter(
            task__project__members=user
        ).select_related(
            "user",
            "task",
            "task__project"
        )

    def perform_create(self, serializer):

        task = serializer.validated_data["task"]

        if self.request.user not in task.project.members.all():
            raise PermissionDenied(
                "You are not a member of this project."
            )

        comment = serializer.save(
            user=self.request.user
        )

        log_activity(
            user=self.request.user,
            project=comment.task.project,
            task=comment.task,
            action="Comment added"
        )

    def perform_destroy(self, instance):

        log_activity(
            user=self.request.user,
            project=instance.task.project,
            task=instance.task,
            action="Comment deleted"
        )

        instance.delete()

    def perform_update(self, serializer):

        comment = serializer.save()

        log_activity(
            user=self.request.user,
            project=comment.task.project,
            task=comment.task,
            action="Comment updated"
        )