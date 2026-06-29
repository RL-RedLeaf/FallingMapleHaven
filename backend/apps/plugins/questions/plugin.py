from ..base import BasePlugin
from ..registry import register_plugin


@register_plugin
class QuestionBoxPlugin(BasePlugin):
    plugin_type = "question_box"
    display_name = "匿名提问箱"
    description = "任何人都可以匿名向你提问"
    icon = "message-question"

    def get_profile_data(self, user_id):
        from .models import AnonymousQuestion
        total = AnonymousQuestion.objects.filter(recipient_id=user_id).count()
        unanswered = AnonymousQuestion.objects.filter(
            recipient_id=user_id, is_answered=False
        ).count()
        return {
            "type": self.plugin_type,
            "name": self.display_name,
            "icon": self.icon,
            "description": self.description,
            "data": {
                "total_questions": total,
                "unanswered_count": unanswered,
            },
            "route": f"/profile/{user_id}/plugins/question-box",
        }
