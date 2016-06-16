from __future__ import unicode_literals

from rest_framework import permissions


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


class IsVisitorSimple(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        base_perm = super(IsVisitorSimple, self).has_permission(request, view)
        if base_perm:
            if hasattr(request.user, 'visitor'):
                return True
        return request.user.is_staff
