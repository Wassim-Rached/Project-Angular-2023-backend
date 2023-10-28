from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed
from authentication.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, permission_classes


#
from .models import CustomUser, Account, JoinClubForm
from .serializers import (
    CustomUserSerializer,
    AccountSerializer,
    ListAccountSerializer,
    AdminAccountSerializer,
    NonAdminAccountSerializer,
    JoinClubFormSerializer,
)
from .permissions import IsAdminOrAccountOwnerOrReadOnly, IsAdminOrJoinClubFormOwner


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


class JoinClubFormViewSet(viewsets.ModelViewSet):
    queryset = JoinClubForm.objects.all()
    serializer_class = JoinClubFormSerializer
    permission_classes = [IsAdminOrJoinClubFormOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {"status": ["exact"]}
    ordering_fields = ["created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_admin:
            return queryset
        return queryset.filter(account=self.request.user.account)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("Updates are not allowed for JoinClubForm.")

    @action(
        detail=True,
        methods=["POST"],
        url_name="accept",
        permission_classes=[IsAdminUser],
    )
    def accept(self, request, pk=None):
        instance = self.get_object()
        instance.accept()
        return Response({"status": instance.status})

    @action(
        detail=True,
        methods=["POST"],
        url_name="reject",
        permission_classes=[IsAdminUser],
    )
    def reject(self, request, pk=None):
        instance = self.get_object()
        instance.reject()
        return Response({"status": instance.status})
