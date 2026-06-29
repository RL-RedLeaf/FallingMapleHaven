from ..base import BasePlugin
from ..registry import register_plugin


@register_plugin
class QuizPlugin(BasePlugin):
    plugin_type = "quiz"
    display_name = "默契问答"
    description = "和朋友互相出题测试默契度"
    icon = "help-circle"

    def get_profile_data(self, user_id):
        from .models import QuizResult
        from django.db.models import Q
        results = QuizResult.objects.filter(
            Q(user_a_id=user_id) | Q(user_b_id=user_id)
        ).order_by("-updated_at")[:5]
        return {
            "type": self.plugin_type,
            "name": self.display_name,
            "icon": self.icon,
            "description": self.description,
            "data": {
                "friend_count": results.count(),
                "top_friends": [
                    {
                        "friend_id": r.user_a_id if r.user_b_id == user_id else r.user_b_id,
                        "match_score": float(r.match_score),
                    }
                    for r in results
                ],
            },
            "route": f"/profile/{user_id}/plugins/quiz",
        }
