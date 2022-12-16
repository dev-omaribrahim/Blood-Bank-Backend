from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    add_fieldsets = (
        (
            None,
            {
                "classes": ("User",),
                "fields": ("username", "email", "user_role", "password1", "password2"),
            },
        ),
    )
