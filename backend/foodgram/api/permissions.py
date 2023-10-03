from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Разрешает доступ для безопасных методов (GET, HEAD, OPTIONS)
        для всех пользователей, а также для аутентифицированных пользователей
        для всех остальных методов.
        """
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Разрешает действия над объектом (например, редактирование и удаление)
        только его автору или администраторам системы.
        Для остальных методов доступ разрешен
        для всех пользователей.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_superuser
