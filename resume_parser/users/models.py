from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Roles constants
    ADMIN = "ADMIN"
    RECRUITER = "RECRUITER"
    CLIENT = "CLIENT"
    CANDIDATE = "CANDIDATE"

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (RECRUITER, "Recruiter"),
        (CLIENT, "Client"),
        (CANDIDATE, "Candidate"),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=CANDIDATE)

    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:
            self.role = self.ADMIN
        return super().save(*args, **kwargs)
