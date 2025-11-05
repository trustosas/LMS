from __future__ import annotations

from django.urls import path

from .views import MeView, UserListCreateView

urlpatterns = [
    path("auth/me", MeView.as_view(), name="auth_me"),
    path("users/", UserListCreateView.as_view(), name="users_list_create"),
]


