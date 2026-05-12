"""Admin registrations for QQMonitor."""

from django.contrib import admin

from qqmonitor.models import QqMonitorEntry


@admin.register(QqMonitorEntry)
class QqMonitorEntryAdmin(admin.ModelAdmin):
    """Admin config for QQ monitor entries."""

    list_display = ("qq_number", "main_character_id", "nickname", "submitted_by", "created_at")
    search_fields = ("qq_number", "main_character_id", "nickname", "submitted_by__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
