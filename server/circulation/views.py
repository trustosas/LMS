from __future__ import annotations

from django.db import transaction
from django.utils.timezone import now
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users.permissions import IsStaffRole
from .models import BorrowRecord
from .serializers import BorrowActionSerializer, BorrowRecordSerializer


class BorrowRecordListView(generics.ListAPIView):
    queryset = BorrowRecord.objects.select_related("borrower", "book").order_by("-id")
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]


class MyActiveBorrowView(generics.GenericAPIView):
    """Get the current user's active borrow record (if any)."""
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            record = BorrowRecord.objects.select_related("book").get(
                borrower=request.user,
                return_date__isnull=True
            )
            return Response(BorrowRecordSerializer(record).data, status=status.HTTP_200_OK)
        except BorrowRecord.DoesNotExist:
            return Response({"book_id": None}, status=status.HTTP_200_OK)


class BorrowBookView(generics.GenericAPIView):
    serializer_class = BorrowActionSerializer
    # Allow any authenticated user; enforce role/ownership and rules below
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        borrower = s.validated_data["borrower"]
        book = s.validated_data["book"]

        # Staff (admin/librarian/superuser) can borrow for anyone; members can only borrow for themselves
        user = request.user
        is_staff_like = bool(getattr(user, "is_superuser", False) or getattr(user, "is_admin", lambda: False)() or getattr(user, "is_librarian", lambda: False)())
        if not is_staff_like and borrower.id != user.id:
            return Response({"detail": "Members can only borrow books for themselves."}, status=status.HTTP_403_FORBIDDEN)

        # Rule: one active borrow per user at a time
        if BorrowRecord.objects.filter(borrower=borrower, return_date__isnull=True).exists():
            return Response({"detail": "You already have an active loan. Please return it before borrowing another."}, status=status.HTTP_400_BAD_REQUEST)

        # Availability
        if book.copies_available <= 0:
            return Response({"detail": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record = BorrowRecord.objects.create(
            borrower=borrower,
            book=book,
            due_date=BorrowRecord.default_due_date(),
        )
        return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED)


class ReturnBookView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    @transaction.atomic
    def post(self, request):
        record_id = request.data.get("borrow_id")
        if not record_id:
            return Response({"detail": "Borrow ID required."}, status=400)
        try:
            record = BorrowRecord.objects.select_for_update().select_related("book").get(pk=record_id)
        except BorrowRecord.DoesNotExist:
            return Response({"detail": "Borrow record not found."}, status=404)

        if record.return_date:
            return Response({"detail": "Already returned."}, status=400)

        record.return_date = now().date()
        record.save(update_fields=["return_date"])

        book = record.book
        book.copies_available += 1
        if book.copies_available > 0:
            book.status = book.STATUS_AVAILABLE
        book.save(update_fields=["copies_available", "status"])

        return Response(BorrowRecordSerializer(record).data)


