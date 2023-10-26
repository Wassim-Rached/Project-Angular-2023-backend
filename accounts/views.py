from rest_framework import viewsets
from rest_framework import permissions

# 
from .models import CustomUser,Account
from .serializers import CustomUserSerializer,AccountSerializer
from .permissions import IsAdminOrSelf


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            # Allow anyone to create an account or retrieve data
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Use the custom permission class to determine if a user can update or delete
            return [IsAdminOrSelf()]
        return super().get_permissions()


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
