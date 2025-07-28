from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        # Allow read to anyone
        if request.method in SAFE_METHODS:
            return True
        # Allow write only to authenticated users
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        # return request.user.is_admin or obj.created_by == request.user
        # Only allow owner or admin to update/delete
        return request.user.is_staff or obj.created_by == request.user
