from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(
        source="user.username"
    )

    project = serializers.ReadOnlyField(
        source="project.name"
    )

    task = serializers.ReadOnlyField(
        source="task.title"
    )

    class Meta:
        model = ActivityLog

        fields = [
            "id",
            "user",
            "project",
            "task",
            "action",
            "created_at",
        ]