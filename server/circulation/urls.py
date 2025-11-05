from __future__ import annotations

from django.urls import path

from .views import BorrowBookView, BorrowRecordListView, MyActiveBorrowView, ReturnBookView

urlpatterns = [
    path("borrow-records", BorrowRecordListView.as_view(), name="borrow_records"),
    path("my-active-borrow", MyActiveBorrowView.as_view(), name="my_active_borrow"),
    path("borrow", BorrowBookView.as_view(), name="borrow_book"),
    path("return", ReturnBookView.as_view(), name="return_book"),
]


