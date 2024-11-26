from rest_framework.permissions import BasePermission

class IsArtist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Artist'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Customer'
