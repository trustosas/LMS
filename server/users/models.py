from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        LIBRARIAN = "LIBRARIAN", "Librarian"
        MEMBER = "MEMBER", "Member"

    role = models.CharField(max_length=16, choices=Role.choices, default=Role.MEMBER)

    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN

    def is_librarian(self) -> bool:
        return self.role == self.Role.LIBRARIAN


