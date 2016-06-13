from __future__ import unicode_literals

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff or obj == request.user


class IsStoreOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(request.user, 'vendor'):
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(request.user, 'vendor'):
            return request.user.id == obj.owner_id

        return request.user.is_staff


class IsOwnerOrReadOnly(IsStoreOwnerOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(request.user, 'vendor'):
            return request.user.id == obj.store.owner_id

        return request.user.is_staff


class IsVisitor(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if view.action == 'create':
            # Allow any user to create mirror instances
            return True
        base_perm = super(IsVisitor, self).has_permission(request, view)
        if base_perm:
            if hasattr(request.user, 'visitor'):
                return True
        return request.user.is_staff
