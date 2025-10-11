# core/permissions.py

from rest_framework import permissions
from .models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        # Allow anyone to view (list or retrieve), but restrict edits to authenticated users
        if view.action in ['list', 'retrieve']:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only permissions for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the object's owner or admin staff
        return obj.owner == request.user or request.user.is_staff


class IsHostUser(permissions.BasePermission):
    """
    Allows access only to authenticated users with the HOST or ADMIN role.
    """
    def has_permission(self, request, view):
        # Must be authenticated AND be a host or admin
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role in [User.Role.HOST, User.Role.ADMIN])
        )
