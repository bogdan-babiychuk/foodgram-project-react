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
