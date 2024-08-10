from rest_framework.permissions import BasePermission


class IsAdminOrOwnerResponse(BasePermission):
    def has_permission(self, request, view):
        if request.session.session_key is None:
            request.session.creat()

        return super().has_permission(request, view)
