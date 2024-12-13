from rest_framework.permissions import BasePermission


class IsDriver(BasePermission):
    """
    Allows access only to drivers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_driver)