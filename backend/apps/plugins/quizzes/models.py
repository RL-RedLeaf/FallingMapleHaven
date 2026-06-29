from django.conf import settings
from django.db import models


class QuizQuestion(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_questions_created"
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_questions_received"
    )
    question = models.TextField()
    correct_answer = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plugins_quizquestion"
        indexes = [models.Index(fields=["creator", "target_user"])]

    def __str__(self):
        return f"Q: {self.question[:30]}"


class QuizAnswer(models.Model):
    question = models.OneToOneField(QuizQuestion, on_delete=models.CASCADE, related_name="answer")
    answerer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plugins_quizanswer"

    def __str__(self):
        return f"Answer: {self.answer}"


class QuizResult(models.Model):
    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results_as_a"
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results_as_b"
    )
    total_questions = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    match_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plugins_quizresult"
        constraints = [
            models.UniqueConstraint(fields=["user_a", "user_b"], name="unique_quiz_result")
        ]

    def __str__(self):
        return f"{self.user_a} vs {self.user_b}: {self.match_score}%"
