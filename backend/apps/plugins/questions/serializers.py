from rest_framework import serializers
from .models import AnonymousQuestion


class AdminQuestionSerializer(serializers.ModelSerializer):
    real_sender = serializers.SerializerMethodField()
    recipient_nickname = serializers.CharField(source="recipient.nickname", read_only=True)

    class Meta:
        model = AnonymousQuestion
        fields = [
            "id", "recipient", "recipient_nickname", "real_sender", "content", "answer",
            "is_answered", "is_public", "created_at", "answered_at",
        ]
        read_only_fields = [
            "id", "recipient", "recipient_nickname", "real_sender", "created_at", "answered_at",
        ]

    def get_real_sender(self, obj):
        return {"user_id": obj.sender.id, "nickname": obj.sender.nickname}


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousQuestion
        fields = [
            "id", "content", "answer", "is_answered", "is_public",
            "created_at", "answered_at",
        ]
        read_only_fields = [
            "id", "created_at", "answered_at",
        ]


class QuestionCreateSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    content = serializers.CharField()
    is_public = serializers.BooleanField(default=True)


class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()
