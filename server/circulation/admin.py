from django.contrib import admin

from .models import BorrowRecord


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "borrower", "book", "borrow_date", "due_date", "return_date", "fine_amount")
    search_fields = ("borrower__username", "book__title", "book__isbn")


