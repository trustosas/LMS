from __future__ import annotations

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Book(models.Model):
    STATUS_AVAILABLE = "available"
    STATUS_BORROWED = "borrowed"
    STATUS_CHOICES = (
        (STATUS_AVAILABLE, "Available"),
        (STATUS_BORROWED, "Borrowed"),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["author"]),
            models.Index(fields=["isbn"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.title} ({self.isbn})"


