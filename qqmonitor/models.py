"""Models for QQMonitor."""

from django.conf import settings
from django.db import models


class QqMonitorEntry(models.Model):
    """User-submitted QQ monitor entry."""

    qq_number = models.CharField("QQ号", max_length=32)
    main_character_id = models.BigIntegerField("主角色ID")
    nickname = models.CharField("昵称", max_length=64)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="qqmonitor_entries",
        verbose_name="提交用户",
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "QQ监控记录"
        verbose_name_plural = "QQ监控记录"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["qq_number", "main_character_id"],
                name="uq_qqmonitor_qq_and_main_character",
            ),
        ]

    def __str__(self):
        return f"{self.nickname} ({self.qq_number})"
