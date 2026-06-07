from rest_framework.permissions import BasePermission


class IsProjectOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        # Admin can do everything
        if request.user.role == "ADMIN":
            return True

        # Safe methods are read-only
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user in obj.members.all()

        # Update/Delete only owner
        return obj.owner == request.user