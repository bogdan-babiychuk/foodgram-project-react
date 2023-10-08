from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-зона пользователя.
    """
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email',)

    search_fields = ('username', 'email')
    list_filter = ('username', 'email',)

    def save_model(self, request, obj, form, change):
        """Шифрует пароль в админке"""
        if not obj.pk and obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
