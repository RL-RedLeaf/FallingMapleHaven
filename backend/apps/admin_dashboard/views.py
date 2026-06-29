from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admin_dashboard.models import SiteLog, SiteSettings
from apps.admin_dashboard.serializers import (
    AdminLogSerializer,
    AdminCommentSerializer,
    AdminPostSerializer,
    AdminSiteSettingsSerializer,
    AdminSiteSettingsUpdateSerializer,
    AdminUserSerializer,
)
from apps.common.utils import api_response
from apps.chat.models import Message
from apps.feed.models import Comment, Post
from apps.plugins.models import Plugin

User = get_user_model()


class AdminPermissionMixin:
    def check_admin(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return api_response(code=40003, message="无权访问", status=status.HTTP_403_FORBIDDEN)
        return None


class AdminUserListView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        search = request.query_params.get("search", "").strip()
        users = User.objects.all()
        if search:
            users = users.filter(
                Q(username__icontains=search)
                | Q(nickname__icontains=search)
                | Q(email__icontains=search)
            )
        users = users.order_by("-date_joined")
        serializer = AdminUserSerializer(users, many=True)
        return api_response(data=serializer.data)


class AdminUserUpdateView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        error = self.check_admin(request)
        if error:
            return error

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return api_response(code=40004, message="用户不存在", status=status.HTTP_404_NOT_FOUND)

        allowed_fields = {"is_active", "is_staff"}
        updates = {key: value for key, value in request.data.items() if key in allowed_fields}
        for key, value in updates.items():
            setattr(user, key, value)
        user.save()

        SiteLog.objects.create(
            user=request.user,
            action="update_user",
            detail={"user_id": pk, "changes": request.data},
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        return api_response(data=AdminUserSerializer(user).data)


class AdminPostListView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        posts = Post.objects.all().order_by("-created_at")
        serializer = AdminPostSerializer(posts, many=True)
        return api_response(data=serializer.data)


class AdminPostDeleteView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        error = self.check_admin(request)
        if error:
            return error

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return api_response(code=40004, message="动态不存在", status=status.HTTP_404_NOT_FOUND)

        post.delete()

        SiteLog.objects.create(
            user=request.user,
            action="delete_post",
            detail={"post_id": pk},
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        return api_response(message="动态已删除")


class AdminCommentListView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        comments = Comment.objects.select_related("author", "post").order_by("-created_at")
        serializer = AdminCommentSerializer(comments, many=True)
        return api_response(data=serializer.data)


class AdminCommentDeleteView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        error = self.check_admin(request)
        if error:
            return error

        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return api_response(code=40004, message="评论不存在", status=status.HTTP_404_NOT_FOUND)

        comment.delete()

        SiteLog.objects.create(
            user=request.user,
            action="delete_comment",
            detail={"comment_id": pk},
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        return api_response(message="评论已删除")


class AdminAnonymousQuestionsView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        from apps.plugins.questions.models import AnonymousQuestion
        from apps.plugins.questions.serializers import AdminQuestionSerializer
        questions = AnonymousQuestion.objects.all().order_by("-created_at")
        serializer = AdminQuestionSerializer(questions, many=True)
        return api_response(data=serializer.data)


class AdminPluginListView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        plugins = Plugin.objects.all()
        data = [
            {
                "id": p.id,
                "name": p.name,
                "type": p.type,
                "is_active": p.is_active,
                "config": p.config,
                "created_at": p.created_at,
            }
            for p in plugins
        ]
        return api_response(data=data)


class AdminPluginUpdateView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        error = self.check_admin(request)
        if error:
            return error

        try:
            plugin = Plugin.objects.get(pk=pk)
        except Plugin.DoesNotExist:
            return api_response(code=40004, message="插件不存在", status=status.HTTP_404_NOT_FOUND)

        is_active = request.data.get("is_active")
        if is_active is not None:
            plugin.is_active = is_active
            plugin.save()

        SiteLog.objects.create(
            user=request.user,
            action="update_plugin",
            detail={"plugin_id": pk, "is_active": is_active},
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        return api_response(data={
            "id": plugin.id,
            "name": plugin.name,
            "type": plugin.type,
            "is_active": plugin.is_active,
            "config": plugin.config,
            "created_at": plugin.created_at,
        })


class AdminSettingsView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        settings = SiteSettings.objects.all()
        serializer = AdminSiteSettingsSerializer(settings, many=True)
        return api_response(data=serializer.data)

    def patch(self, request):
        error = self.check_admin(request)
        if error:
            return error

        serializer = AdminSiteSettingsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        settings_data = serializer.validated_data["settings"]
        for key, value in settings_data.items():
            SiteSettings.objects.update_or_create(key=key, defaults={"value": value})

        SiteLog.objects.create(
            user=request.user,
            action="update_settings",
            detail={"settings": settings_data},
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        settings = SiteSettings.objects.all()
        out_serializer = AdminSiteSettingsSerializer(settings, many=True)
        return api_response(data=out_serializer.data)


class AdminStatsView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        data = {
            "total_users": User.objects.count(),
            "total_posts": Post.objects.count(),
            "total_comments": Comment.objects.count(),
            "total_messages": Message.objects.count(),
            "active_users_today": User.objects.filter(last_login__date__gte=timezone.now().date()).count(),
        }
        return api_response(data=data)


class AdminLogsView(APIView, AdminPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        error = self.check_admin(request)
        if error:
            return error

        logs = SiteLog.objects.all()[:100]
        serializer = AdminLogSerializer(logs, many=True)
        return api_response(data=serializer.data)
