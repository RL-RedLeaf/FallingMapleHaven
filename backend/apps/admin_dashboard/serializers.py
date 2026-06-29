from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.admin_dashboard.models import SiteSettings, SiteLog
from apps.feed.models import Post, Comment

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "nickname", "email", "is_active", "is_staff", "is_superuser", "date_joined", "last_login"]


class AdminPostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source="author.nickname")

    class Meta:
        model = Post
        fields = ["id", "author_nickname", "content", "visibility", "topic_tag", "created_at"]


class AdminCommentSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source="author.nickname")
    post_content = serializers.CharField(source="post.content")

    class Meta:
        model = Comment
        fields = ["id", "post", "post_content", "author_nickname", "content", "parent", "created_at"]


class AdminSiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ["key", "value"]


class AdminSiteSettingsUpdateSerializer(serializers.Serializer):
    settings = serializers.DictField(child=serializers.JSONField())


class AdminLogSerializer(serializers.ModelSerializer):
    admin_nickname = serializers.SerializerMethodField()

    class Meta:
        model = SiteLog
        fields = ["id", "admin_nickname", "action", "detail", "ip_address", "created_at"]

    def get_admin_nickname(self, obj):
        return obj.user.nickname if obj.user else "系统"
