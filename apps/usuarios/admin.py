from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Extra Fields', {'fields': ('tipo_usuario', 'id_cliente',)}),)


admin.site.register(User, CustomUserAdmin)
