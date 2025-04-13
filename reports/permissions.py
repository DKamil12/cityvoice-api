from rest_framework import permissions

class IsReportOwnerOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        return request.user == request.report.user