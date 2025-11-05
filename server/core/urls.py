from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth
    path("api/auth/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # Apps
    path("api/", include("users.urls")),
    path("api/", include("catalog.urls")),
    path("api/", include("circulation.urls")),
    path("api/", include("reports.urls")),
]


