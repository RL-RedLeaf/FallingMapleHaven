from django.conf import settings
from django.db import models


class AnonymousQuestion(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_questions"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_questions"
    )
    content = models.TextField()
    answer = models.TextField(null=True, blank=True)
    is_answered = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "plugins_anonymousquestion"
        indexes = [models.Index(fields=["recipient", "-created_at"])]

    def __str__(self):
        return f"Question for {self.recipient}: {self.content[:30]}"
