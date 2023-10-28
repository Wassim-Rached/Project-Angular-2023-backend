from django_filters.rest_framework import DjangoFilterBackend
from authentication.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets, status


#
from .models import CustomUser, Account
from .serializers import (
    CustomUserSerializer,
    AccountSerializer,
    ListAccountSerializer,
    AdminAccountSerializer,
    NonAdminAccountSerializer,
)
from .permissions import IsAdminOrAccountOwnerOrReadOnly


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {"username": ["icontains"]}
    ordering_fields = ["date_joined"]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrAccountOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {"user__username": ["icontains"]}
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListAccountSerializer

        if self.request.user.is_admin:
            return AdminAccountSerializer

        return NonAdminAccountSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        if user:
            user.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
