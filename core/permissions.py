# In core/permissions.py

from rest_framework import permissions
from .models import User # Make sure to import your custom User model

class IsHostOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow hosts or admins to edit or create objects.
    Allows any user (authenticated or not) to view (read-only).
    """

    def has_permission(self, request, view):
        # Allow read-only (GET, HEAD, OPTIONS) requests for everyone.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write (POST, PUT, DELETE) requests, we require the user to be authenticated
        # AND have the role of either HOST or ADMIN.
        # The user must be authenticated for request.user.role to exist.
        return request.user and request.user.is_authenticated and (request.user.role in [User.Role.HOST, User.Role.ADMIN])
    
class IsHostUser(permissions.BasePermission):
    """
    Allows access only to authenticated users with the HOST or ADMIN role.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role in [User.Role.HOST, User.Role.ADMIN])
        )
