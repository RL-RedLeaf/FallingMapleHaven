from django.conf import settings
from django.db import models


class Friendship(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "待确认"
        ACCEPTED = "accepted", "已接受"
        REJECTED = "rejected", "已拒绝"

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendships_received",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "friends_friendship"
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"],
                name="uq_friendship_from_to",
            ),
            models.CheckConstraint(
                check=~models.Q(from_user=models.F("to_user")),
                name="ck_friendship_no_self",
            ),
        ]

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"
