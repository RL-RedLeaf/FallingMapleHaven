from django.contrib import admin

from .models import SiteLog, SiteSettings


@admin.register(SiteLog)
class SiteLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("user__username", "action")
    readonly_fields = ("user", "action", "detail", "ip_address", "created_at")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "updated_at")
    search_fields = ("key",)
