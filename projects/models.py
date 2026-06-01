from django.db import models
from django.conf import settings

# Create your models here.

class Project(models.Model):

    class Status(models.TextChoices):
        PLANNING = "PLANNING", "Planning"
        ACTIVE = "ACTIVE", "Active"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"


    name = models.CharField(max_length=255, default="Untitled Project")
    description = models.TextField(verbose_name="Project Details")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="projects",
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices = Status.choices,
        default=Status.PLANNING
    )

    is_archived = models.BooleanField(default=False)

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null = True,
        blank = True

    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username