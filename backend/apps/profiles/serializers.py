from rest_framework import serializers
from django.utils import timezone
from apps.accounts.models import User
from apps.profiles.models import UserProfile, VisitRecord, GuestbookEntry


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    real_name = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    visitor_count = serializers.SerializerMethodField()
    plugins = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "user_id", "nickname", "avatar_url", "cover_url",
            "bio", "real_name", "show_real_name", "date_joined",
            "visitor_count", "plugins", "visitor_public", "layout_config",
        ]

    def get_user_id(self, obj):
        return obj.user.id

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_avatar_url(self, obj):
        return obj.user.avatar.url if obj.user.avatar else None

    def get_cover_url(self, obj):
        return obj.user.cover_image.url if obj.user.cover_image else None

    def get_bio(self, obj):
        return obj.user.bio

    def get_real_name(self, obj):
        return obj.user.real_name

    def get_date_joined(self, obj):
        return obj.user.date_joined

    def get_visitor_count(self, obj):
        return VisitRecord.objects.filter(visited_user=obj.user).count()

    def get_plugins(self, obj):
        from apps.plugins.registry import PluginRegistry
        return PluginRegistry.get_profile_plugins(obj.user.id)


class VisitorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="visitor.id")
    nickname = serializers.CharField(source="visitor.nickname")
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = VisitRecord
        fields = ["user_id", "nickname", "avatar_url", "visited_at"]

    def get_avatar_url(self, obj):
        return obj.visitor.avatar.url if obj.visitor.avatar else None


class GuestbookEntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = GuestbookEntry
        fields = ["id", "user", "content", "reply", "replied_at", "created_at"]

    def get_user(self, obj):
        return {
            "user_id": obj.author.id,
            "nickname": obj.author.nickname,
            "avatar_url": obj.author.avatar.url if obj.author.avatar else None,
        }


class GuestbookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestbookEntry
        fields = ["content"]
        extra_kwargs = {"content": {"required": True}}


class GuestbookReplySerializer(serializers.Serializer):
    reply = serializers.CharField(required=True)
