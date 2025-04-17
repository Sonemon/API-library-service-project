from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """

    def has_permission(self, request, view):
        # Check if the request method is safe (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Otherwise, only allow admins to edit
        return request.user and request.user.is_staff
