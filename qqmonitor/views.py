"""Views for QQMonitor."""

from django.contrib import messages
from django.shortcuts import render

from allianceauth.authentication.decorators import main_character_required
from qqmonitor.forms import QqMonitorEntryForm
from qqmonitor.models import QqMonitorEntry


@main_character_required
def index(request):
    """Plugin home page."""
    if request.method == "POST":
        form = QqMonitorEntryForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            existing = QqMonitorEntry.objects.filter(
                qq_number=cleaned["qq_number"],
                main_character_id=cleaned["main_character_id"],
            ).first()
            old_nickname = existing.nickname if existing else None
            _, created = QqMonitorEntry.objects.update_or_create(
                qq_number=cleaned["qq_number"],
                main_character_id=cleaned["main_character_id"],
                defaults={"nickname": cleaned["nickname"], "submitted_by": request.user},
            )
            if created:
                messages.success(request, "提交成功。")
            else:
                if old_nickname != cleaned["nickname"]:
                    messages.success(request, "已存在同主角色记录，昵称已更新。")
                else:
                    messages.success(request, "该记录已存在，信息保持不变。")
            form = QqMonitorEntryForm()
    else:
        form = QqMonitorEntryForm()

    context = {
        "page_title": "QQ Monitor",
        "form": form,
    }
    return render(request, "qqmonitor/index.html", context)
