from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import Book
from .models import BorrowRecord


class BorrowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="m", password="p")
        self.book = Book.objects.create(title="X", author="Y", isbn="9780000000099", copies_total=2, copies_available=2)

    def test_borrow_updates_availability(self):
        r = BorrowRecord.objects.create(borrower=self.user, book=self.book, due_date=BorrowRecord.default_due_date())
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 1)
        self.assertIsNotNone(r.pk)


