from rest_framework import permissions

from user.models import Profile


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.pk == request.user.pk


class RejectAll(permissions.BasePermission):

    def has_permission(self, request, view):
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsOwnerOrReject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerProfileOrReject(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_buyer and request.user.profile

    def has_object_permission(self, request, view, obj):
        if type(obj).__name__ == 'OrderItem':
            return obj.order.profile == request.user.profile
        return obj.profile == request.user.profile


class IsDropShipperOrReject(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == Profile.ROLE.DROPSHIPPER


class IsBuyerProfileOrReject(permissions.BasePermission):

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile')
