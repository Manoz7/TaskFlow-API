from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        DEVELOPER = "DEVELOPER", "Developer"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices = Role.choices,
        default=Role.DEVELOPER
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
