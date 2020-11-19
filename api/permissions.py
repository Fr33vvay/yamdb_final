from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission разрешающий доступ к редактированию объекта только
    администратору. Для чтения доступно всем.
    """

    message = 'Недостаточные права для данного действия.'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                (request.user.is_authenticated and request.user.is_admin)
                )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_admin


class IsAdminModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission для доступа к редактированию объекта: только админам,
    модераторам и автору. Для чтения доступ всем.
    """

    message = 'Недостаточные права для данного действия.'

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                (request.user.is_admin or request.user.is_moderator) or
                obj.author == request.user
                )


class IsAdministrator(permissions.BasePermission):
    """
    Permissions для проверки наличия статуса Администратора.
    """

    message = 'Вам необходимы соответствующие права доступа.'

    def has_permission(self, request, view):
        return request.user.is_admin


class IsModerator(permissions.BasePermission):
    """
    Permissions для проверки наличия статуса Модератора.
    """

    message = 'Вам необходимы соответствующие права доступа.'

    def has_permission(self, request, view):
        return request.user.is_moderator
