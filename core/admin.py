from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Регистрация админки"""
    empty_value_display = '-empty-'
    # exclude = ('password',)
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('is_staff', 'is_active', 'is_superuser',)
    search_fields = ['first_name', 'last_name', 'username']
    readonly_fields = ('last_login', 'date_joined',)


admin.site.unregister(Group)
