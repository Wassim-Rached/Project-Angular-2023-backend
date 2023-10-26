from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admin users to perform any action
        if request.user.is_staff:
            return True

        # Allow users to perform GET (retrieve) requests
        if request.method == 'GET':
            return True

        # Allow users to perform POST (create) requests
        if request.method == 'POST':
            return True

        # Allow users to update or delete their own account
        return obj == request.user
