from __future__ import unicode_literals

from rest_framework import permissions


class VisitorBasic(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        base_perm = super(VisitorBasic, self).has_permission(request, view)
        if base_perm:
            if hasattr(request.user, 'visitor'):
                return True
        return request.user.is_staff


class IsOwnerOrMember(VisitorBasic):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and not obj.is_private:
            return True

        if hasattr(request.user, 'visitor'):
            user = request.user
            if user.id == obj.owner_id:
                return True
            elif request.method == 'GET' and \
                    obj.member_set.filter(visitor_id=user.id).exists():
                return True

        return request.user.is_staff


class CanServeTags(VisitorBasic):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and not obj.is_private:
            return True

        if hasattr(request.user, 'visitor'):
            user = request.user
            if user.id == obj.group.owner_id:
                return True
            elif user.id == obj.visitor_id and\
                    obj.group.member_set.filter(visitor_id=user.id).exists():
                return True
        return request.user.is_staff
