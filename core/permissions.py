from rest_framework import permissions


class IsBlogOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owner of an blog to edit it.
    Assumes the model instance has an `blog` or 'owner attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'owner'):
            return obj.owner.user == request.user
        
        if hasattr(obj, 'blog'):
            return obj.blog.owner.user == request.user
