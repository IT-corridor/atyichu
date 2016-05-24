from __future__ import unicode_literals

from rest_framework import permissions


class IsStoreOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff or request.user.id == obj.owner_id
