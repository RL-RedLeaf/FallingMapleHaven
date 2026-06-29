from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/friends/", include("apps.friends.urls")),
    path("api/v1/posts/", include("apps.feed.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/chat/", include("apps.chat.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/groups/", include("apps.groups.urls")),
    path("api/v1/admin/", include("apps.admin_dashboard.urls")),
    path("api/v1/plugins/", include("apps.plugins.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
