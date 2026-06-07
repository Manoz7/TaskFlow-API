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

        project = attrs.get(
            "project",
            self.instance.project if self.instance else None
        )

        assignee = attrs.get(
            "assignee",
            self.instance.assignee if self.instance else None
        )

        if assignee and project:
            if assignee not in project.members.all():
                raise serializers.ValidationError(
                    "Assignee must be a member of the project."
                )

        return attrs
    
    def validate_status(self, value):

        if not self.instance:
            return value

        request = self.context.get("request")

        # Admin and Manager can override workflow
        if (
            request
            and request.user.role in ["ADMIN", "MANAGER"]
        ):
            return value

        current_status = self.instance.status

        allowed_transitions = {
            "TODO": ["IN_PROGRESS"],

            "IN_PROGRESS": [
                "BLOCKED",
                "COMPLETED"
            ],

            "BLOCKED": [
                "IN_PROGRESS"
            ],

            "COMPLETED": []
        }

        if value != current_status:

            if value not in allowed_transitions[current_status]:

                raise serializers.ValidationError(
                    f"Cannot move task from "
                    f"{current_status} to {value}"
                )

        return value