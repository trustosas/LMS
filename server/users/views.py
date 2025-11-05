from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .permissions import IsAdmin
from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("id")
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


