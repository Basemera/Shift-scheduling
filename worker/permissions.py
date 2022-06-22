from rest_framework import permissions

class SupervisorAllActions(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_supervisor_or_admin():
            return True
         
        # return super().has_object_permission(request, view, obj)