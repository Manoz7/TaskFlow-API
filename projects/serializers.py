from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):

    owner_email = serializers.ReadOnlyField(
        source = "owner.email"
    )

    class Meta:
        model = Project

        fields = [
            "id",
            "name",
            "description",
            "owner",
            "owner_email",
            "members",
            "status",
            "is_archived",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):

        queryset = Project.objects.filter(
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )
        
        if queryset.exists():
            raise serializers.ValidationError(
                "Project with this name already exists!!"
            )

        return value
 

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError(
                    {
                        "end_date":
                        "End date cannot be earlier than start date!!"
                    }
                )
        return attrs
    

    def create(self, validated_data):
        request = self.context["request"]

        project = Project.objects.create(
            owner= request.user,
            **validated_data
        )

        project.members.add(request.user)

        return object