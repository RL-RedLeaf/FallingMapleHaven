from django.conf import settings
from django.db import models


class SiteLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=100)
    detail = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_sitelog"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} by {self.user}"


class SiteSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admin_sitesettings"

    def __str__(self):
        return self.key
