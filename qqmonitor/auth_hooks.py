"""Hook registrations for AllianceAuth."""

from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from qqmonitor import urls


class QqMonitorMenuItem(MenuItemHook):
    """Sidebar entry for QQMonitor."""

    def __init__(self):
        super().__init__(
            _("QQ Monitor"),
            "fas fa-bell fa-fw",
            "qqmonitor:index",
            navactive=["qqmonitor:"],
        )

    def render(self, request):
        """Render menu item for authenticated users."""
        if request.user.is_authenticated:
            return super().render(request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """Register sidebar menu entry."""
    return QqMonitorMenuItem()


@hooks.register("url_hook")
def register_urls():
    """Register plugin URL routes."""
    return UrlHook(urls, "qqmonitor", r"^qqmonitor/")
