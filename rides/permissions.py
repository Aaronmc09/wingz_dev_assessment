from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allow access only to users whose role is 'admin'.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'
