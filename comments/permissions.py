from rest_framework.permissions import BasePermission


class IsCommentOwnerOrAdminManager(BasePermission):
    """
    Comment owner can edit/delete.
    Admins and Managers can manage any comment.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if request.user.role in ["ADMIN", "MANAGER"]:
            return True

        return obj.user == request.user