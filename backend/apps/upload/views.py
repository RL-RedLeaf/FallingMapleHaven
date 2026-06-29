import os
import uuid

from django.conf import settings
from PIL import Image
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from apps.common.utils import api_response

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return api_response(code=40001, message="请上传文件", data=None, status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(file.name)[1].lower()
        safe_filename = f"{uuid.uuid4().hex}{ext}"
        subdir = "uploads"
        upload_dir = settings.MEDIA_ROOT / subdir
        upload_dir.mkdir(parents=True, exist_ok=True)
        filepath = upload_dir / safe_filename
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        url = f"{settings.MEDIA_URL}{subdir}/{safe_filename}"
        return api_response(data={"url": url})


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return api_response(code=40001, message="请上传图片", data=None, status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            return api_response(code=40001, message="仅支持 jpg/png/gif/webp 格式", data=None, status=status.HTTP_400_BAD_REQUEST)

        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)
        except Exception:
            return api_response(code=40001, message="文件不是有效的图片", data=None, status=status.HTTP_400_BAD_REQUEST)

        safe_filename = f"{uuid.uuid4().hex}{ext}"
        subdir = "uploads"
        upload_dir = settings.MEDIA_ROOT / subdir
        upload_dir.mkdir(parents=True, exist_ok=True)
        filepath = upload_dir / safe_filename
        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        url = f"{settings.MEDIA_URL}{subdir}/{safe_filename}"
        return api_response(data={"url": url})
