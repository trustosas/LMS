from __future__ import annotations

from datetime import timedelta

from django.db.models import Count
from django.utils.timezone import now
from rest_framework import permissions, views
from rest_framework.response import Response

from circulation.models import BorrowRecord
from users.permissions import IsStaffRole


class CirculationSummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def get(self, request):
        range_param = request.query_params.get("range", "week")
        days = 1 if range_param == "day" else 7 if range_param == "week" else 30
        since = (now() - timedelta(days=days)).date()

        total_borrowed = BorrowRecord.objects.filter(borrow_date__gte=since).count()
        total_returned = BorrowRecord.objects.filter(return_date__gte=since).count()
        payload = {
            "since": str(since),
            "total_borrowed": total_borrowed,
            "total_returned": total_returned,
        }
        return Response(payload)


class TopBorrowedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        data = (
            BorrowRecord.objects.values("book__id", "book__title", "book__author")
            .annotate(times=Count("id"))
            .order_by("-times")[:limit]
        )
        return Response(list(data))


