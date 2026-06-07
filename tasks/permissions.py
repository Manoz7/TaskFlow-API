from rest_framework.permissions import BasePermission


class IsProjectMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user in obj.project.members.all()


class CanManageTask(BasePermission):

    def has_permission(self, request, view):

        if request.method == "POST":
            return request.user.role in [
                "ADMIN",
                "MANAGER"
            ]

        return True

    def has_object_permission(self, request, view, obj):

        if request.user.role in [
            "ADMIN",
            "MANAGER"
        ]:
            return True

        if request.method in ["PUT", "PATCH"]:
            return obj.assignee == request.user

        return False