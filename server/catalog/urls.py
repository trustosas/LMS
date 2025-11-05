from __future__ import annotations

from django.urls import path

from .views import BookListCreateView, BookRetrieveUpdateView

urlpatterns = [
    path("books", BookListCreateView.as_view(), name="book_list_create"),
    path("books/<int:pk>", BookRetrieveUpdateView.as_view(), name="book_retrieve_update"),
]


