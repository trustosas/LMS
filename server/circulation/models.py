from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.db import models

from catalog.models import Book


class BorrowRecord(models.Model):
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrow_records")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        if creating:
            # Maintain book availability on create
            book = self.book
            if book.copies_available > 0:
                book.copies_available -= 1
                if book.copies_available == 0:
                    book.status = Book.STATUS_BORROWED
                book.save(update_fields=["copies_available", "status"])

    @staticmethod
    def default_due_date():
        from django.utils.timezone import now

        return (now() + timedelta(days=14)).date()


