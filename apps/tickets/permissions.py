from rest_framework.permissions import BasePermission

from apps.users.models import User

class                                                                                                   isSupportAdmin(BasePermission):
    message = "Only support admins can perform this action."
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == User.Role.SUPPORT_ADMIN)

class IsSupportAgent(BasePermission):
    message = "Only support agents can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.SUPPORT_AGENT
        )


class IsCustomer(BasePermission):
    message = "Only customers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.CUSTOMER
        )    