from rest_framework import permissions


class IsAdminOrAccountOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            # Check if the user is an admin
            if request.user.is_admin:
                return True

            # Check if the user is the owner of the account
            if request.user.account == obj:
                return True

        return False
