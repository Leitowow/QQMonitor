"""App configuration for QQMonitor."""

from django.apps import AppConfig

from qqmonitor import __version__


class QqmonitorConfig(AppConfig):
    """QQMonitor app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "qqmonitor"
    label = "qqmonitor"
    verbose_name = f"QQ Monitor v{__version__}"
