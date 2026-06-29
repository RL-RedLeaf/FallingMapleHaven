from django.urls import path

from apps.accounts.views import (
    AvatarUploadView,
    ChangePasswordView,
    CoverUploadView,
    CsrfTokenView,
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
)

urlpatterns = [
    path("csrf/", CsrfTokenView.as_view(), name="auth-csrf"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    path("avatar/", AvatarUploadView.as_view(), name="auth-avatar"),
    path("cover/", CoverUploadView.as_view(), name="auth-cover"),
]
