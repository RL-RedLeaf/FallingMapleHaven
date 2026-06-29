from django.urls import path
from apps.plugins.quizzes.views import (
    QuizQuestionCreateView,
    QuizReceivedQuestionsView,
    QuizAnswerView,
    QuizResultView,
)

urlpatterns = [
    path("questions/", QuizQuestionCreateView.as_view(), name="quiz-create"),
    path("questions/received/", QuizReceivedQuestionsView.as_view(), name="quiz-received"),
    path("questions/<int:pk>/answer/", QuizAnswerView.as_view(), name="quiz-answer"),
    path("result/<int:friend_id>/", QuizResultView.as_view(), name="quiz-result"),
]
