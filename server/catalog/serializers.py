from __future__ import annotations

from rest_framework import serializers

from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "isbn",
            "category",
            "category_id",
            "publication_year",
            "copies_total",
            "copies_available",
            "status",
        ]
        read_only_fields = ["id", "copies_available", "status"]


