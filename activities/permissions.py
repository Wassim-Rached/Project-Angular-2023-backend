from rest_framework import permissions

class IsObjectOwnerOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only authenticated users are allowed
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_admin:
            return True

        # Authenticated users can read their own objects
        if request.method in permissions.SAFE_METHODS and obj.account == request.user.account:
            return True

        # Authenticated users can create, update, and delete their own objects
        return obj.account == request.user.account
