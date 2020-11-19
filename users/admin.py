from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdminBoard(UserAdmin):
    """
    Панель управления пользователями.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
