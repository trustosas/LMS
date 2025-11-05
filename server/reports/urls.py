from __future__ import annotations

from django.urls import path

from .views import CirculationSummaryView, TopBorrowedView

urlpatterns = [
    path("reports/circulation-summary", CirculationSummaryView.as_view(), name="circulation_summary"),
    path("reports/top-borrowed", TopBorrowedView.as_view(), name="top_borrowed"),
]


