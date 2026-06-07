from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "project",
            "assignee",
            "created_by",
            "due_date",
            "estimated_hours",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        project = attrs.get("project")
        assignee = attrs.get("assignee")

        if assignee and project:
            if assignee not in project.members.all():
                raise serializers.ValidationError(
                    "Assignee must be a member of the project."
                )

        return attrs