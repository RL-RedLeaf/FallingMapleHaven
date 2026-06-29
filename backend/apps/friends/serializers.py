from rest_framework import serializers
from apps.friends.models import Friendship
from apps.accounts.models import User


class FriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()


class FriendHandleSerializer(serializers.Serializer):
    request_id = serializers.IntegerField(required=False)
    from_user_id = serializers.IntegerField(required=False)
    action = serializers.ChoiceField(choices=["accept", "reject"])


class UnfriendSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField()


class UserSearchSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar", "avatar_url"]

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None


class FriendSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ["id", "nickname", "avatar_url", "created_at"]

    def get_id(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        return obj.to_user_id if obj.from_user == request.user else obj.from_user_id

    def get_nickname(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        friend = obj.to_user if obj.from_user == request.user else obj.from_user
        return friend.nickname

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        friend = obj.to_user if obj.from_user == request.user else obj.from_user
        return friend.avatar.url if friend.avatar else None


class FriendRequestReceivedSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="from_user.nickname")
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ["id", "nickname", "from_user", "created_at"]

    def get_from_user(self, obj):
        return {
            "user_id": obj.from_user.id,
            "nickname": obj.from_user.nickname,
            "avatar_url": obj.from_user.avatar.url if obj.from_user.avatar else None,
        }
