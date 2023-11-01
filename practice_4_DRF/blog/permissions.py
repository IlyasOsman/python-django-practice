from rest_framework import permissions


class IsBlogAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.authors.all() and request.user.is_member
