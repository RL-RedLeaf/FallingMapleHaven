from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "nickname", "email", "is_staff", "is_superuser", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "nickname", "email")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("个人信息", {"fields": ("nickname", "real_name", "email", "bio", "avatar", "cover_image")}),
        ("权限", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("时间信息", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    filter_horizontal = ("permissions",)
