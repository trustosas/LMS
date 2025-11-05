from __future__ import annotations

from rest_framework import filters, generics, permissions

from users.permissions import IsStaffRole
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author", "isbn"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsStaffRole()]
        return [permissions.IsAuthenticated()]


class BookRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [permissions.IsAuthenticated(), IsStaffRole()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        instance = self.get_object()
        old_total = instance.copies_total
        new_total = serializer.validated_data.get('copies_total', old_total)
        
        # Save the serializer first to update copies_total
        serializer.save()
        
        # Refresh instance from database to get updated values
        instance.refresh_from_db()
        
        # Calculate the difference
        diff = new_total - old_total
        
        # If total copies increased, increase available copies by the same amount
        if diff > 0:
            instance.copies_available += diff
            # Update status if copies become available
            if instance.copies_available > 0 and instance.status == Book.STATUS_BORROWED:
                instance.status = Book.STATUS_AVAILABLE
            instance.save(update_fields=['copies_available', 'status'])


