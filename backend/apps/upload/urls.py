from django.urls import path

from .views import FileUploadView, ImageUploadView

urlpatterns = [
    path("", FileUploadView.as_view(), name="upload-file"),
    path("image/", ImageUploadView.as_view(), name="upload-image"),
]
