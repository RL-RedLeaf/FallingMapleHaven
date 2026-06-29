from django.urls import include, path
from apps.plugins.views import ActivePluginsView

urlpatterns = [
    path("", ActivePluginsView.as_view(), name="plugin-list"),
    path("quiz/", include("apps.plugins.quizzes.urls")),
    path("question-box/", include("apps.plugins.questions.urls")),
]
