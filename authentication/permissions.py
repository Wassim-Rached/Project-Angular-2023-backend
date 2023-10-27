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



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the request method is a safe method (GET, HEAD, or OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is authenticated and is an admin
        if request.user.is_authenticated:
            return request.user.is_admin;

        # If neither of the above conditions is met, deny access
        return False