from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from apps.friends.models import Friendship
from .models import QuizQuestion, QuizAnswer, QuizResult

User = get_user_model()


class QuizQuestionCreateSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()
    question = serializers.CharField()
    correct_answer = serializers.CharField(max_length=500)

    def validate_target_user_id(self, value):
        request = self.context.get("request")
        if not request:
            return value

        if value == request.user.id:
            raise serializers.ValidationError("不能给自己出题")

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("目标用户不存在")

        is_friend = Friendship.objects.filter(
            Q(from_user=request.user, to_user_id=value) | Q(from_user_id=value, to_user=request.user),
            status=Friendship.Status.ACCEPTED,
        ).exists()
        if not is_friend:
            raise serializers.ValidationError("只能向好友出题")

        return value


class QuizQuestionSerializer(serializers.ModelSerializer):
    has_answered = serializers.SerializerMethodField()
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestion
        fields = ["id", "from_user", "target_user", "question", "created_at", "has_answered"]
        read_only_fields = ["id", "from_user", "target_user", "created_at"]

    def get_has_answered(self, obj):
        return hasattr(obj, "answer") and obj.answer is not None

    def get_from_user(self, obj):
        return {
            "user_id": obj.creator.id,
            "nickname": obj.creator.nickname,
            "avatar_url": obj.creator.avatar.url if obj.creator.avatar else None,
        }


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ["id", "question", "answer", "is_correct", "created_at"]
        read_only_fields = ["id", "question", "is_correct", "created_at"]


class QuizResultSerializer(serializers.ModelSerializer):
    friend_id = serializers.SerializerMethodField()

    class Meta:
        model = QuizResult
        fields = ["friend_id", "total_questions", "correct_count", "match_score", "updated_at"]

    def get_friend_id(self, obj):
        user_id = self.context.get("user_id")
        if user_id == obj.user_a_id:
            return obj.user_b_id
        return obj.user_a_id
