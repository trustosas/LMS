from django.test import TestCase

from .models import Book


class BookModelTests(TestCase):
    def test_create_book(self):
        b = Book.objects.create(title="T", author="A", isbn="9780000000010", copies_total=1, copies_available=1)
        self.assertEqual(str(b), "T (9780000000010)")


