from django.urls import path
from apps.plugins.questions.views import (
    QuestionCreateView,
    InboxView,
    AnswerView,
    QuestionDeleteView,
)

urlpatterns = [
    path("", QuestionCreateView.as_view(), name="question-create"),
    path("inbox/", InboxView.as_view(), name="question-inbox"),
    path("<int:pk>/answer/", AnswerView.as_view(), name="question-answer"),
    path("<int:pk>/delete/", QuestionDeleteView.as_view(), name="question-delete"),
]
