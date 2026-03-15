from rest_framework.permissions import BasePermission

from users.models import User


class IsAdminUser(BasePermission):
    """
    Allow access only to users whose custom User model role is 'admin'.
    Links Django auth user to the custom User model via email.
    Caches the lookup on the request to avoid repeated queries.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        custom_user = getattr(request, '_cached_custom_user', None)
        if custom_user is None:
            try:
                custom_user = User.objects.get(email=request.user.email)
            except User.DoesNotExist:
                custom_user = False
            request._cached_custom_user = custom_user

        return custom_user and custom_user.role == User.Role.ADMIN
