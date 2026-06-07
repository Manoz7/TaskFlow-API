from django.shortcuts import render
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdminOrManager
from .permissions import IsProjectOwnerOrAdmin
from rest_framework.exceptions import PermissionDenied


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsProjectOwnerOrAdmin
    ]

    def get_queryset(self):

        user = self.request.user

        if user.role == "ADMIN":
            return Project.objects.all()

        return Project.objects.filter(
            members=user
        )

    def perform_create(self, serializer):

        if self.request.user.role not in [
            "ADMIN",
            "MANAGER"
        ]:
            raise PermissionDenied(
                "Only Admins and Managers can create projects."
            )

        serializer.save()