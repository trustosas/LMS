from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from catalog.models import Book
from .models import BorrowRecord

User = get_user_model()


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "borrower",
            "book",
            "borrow_date",
            "due_date",
            "return_date",
            "fine_amount",
        ]
        read_only_fields = ["id", "borrow_date", "fine_amount"]


class BorrowActionSerializer(serializers.Serializer):
    book_id = serializers.PrimaryKeyRelatedField(source="book", queryset=Book.objects.all())
    borrower_id = serializers.PrimaryKeyRelatedField(source="borrower", queryset=User.objects.all())


