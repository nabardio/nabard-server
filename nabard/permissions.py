from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if isinstance(obj, get_user_model()):
            return request.user.pk == obj.pk
        return request.user == obj.owner
