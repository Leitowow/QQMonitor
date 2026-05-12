"""Views for QQMonitor."""

import hashlib
import hmac
import json
import logging
import time

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from allianceauth.authentication.decorators import main_character_required
from allianceauth.authentication.models import State
from qqmonitor.forms import QqMonitorEntryForm
from qqmonitor.models import QqMonitorEntry

logger = logging.getLogger(__name__)


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


def _json_error(message, status=400):
    return JsonResponse({"ok": False, "error": message}, status=status)


def _get_request_payload(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _is_valid_signature(token, timestamp, qq_number, signature, secret):
    message = f"{token}.{timestamp}.{qq_number}".encode("utf-8")
    expected = hmac.new(
        secret.encode("utf-8"),
        message,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def _get_member_alliance_ids():
    member_state = State.objects.filter(name__iexact="Member").first()
    if not member_state:
        return set()
    return set(member_state.member_alliances.values_list("alliance_id", flat=True))


def _is_user_in_current_alliance(user, member_alliance_ids):
    profile = getattr(user, "profile", None)
    main_character = getattr(profile, "main_character", None)
    alliance_id = getattr(main_character, "alliance_id", None) if main_character else None
    if member_alliance_ids:
        return alliance_id in member_alliance_ids, alliance_id

    # Fallback: if Member state's alliance list is empty, trust AA's assigned state.
    state_name = getattr(getattr(profile, "state", None), "name", "")
    return state_name.lower() == "member", alliance_id


@csrf_exempt
@require_POST
def api_verify_qq(request):
    token = request.headers.get("X-QQM-TOKEN", "")
    timestamp_raw = request.headers.get("X-QQM-TIMESTAMP", "")
    signature = request.headers.get("X-QQM-SIGNATURE", "").lower()

    expected_token = getattr(settings, "QQMONITOR_API_TOKEN", "")
    secret = getattr(settings, "QQMONITOR_API_SECRET", "")
    max_skew_seconds = int(getattr(settings, "QQMONITOR_API_MAX_SKEW_SECONDS", 300))

    if not expected_token or not secret:
        logger.error("QQMonitor API is not configured: missing token or secret.")
        return _json_error("API not configured", status=503)
    if not token or not timestamp_raw or not signature:
        return _json_error("Missing authentication headers", status=401)
    if token != expected_token:
        logger.warning("QQMonitor API authentication failed: invalid token.")
        return _json_error("Invalid token or signature", status=401)

    try:
        timestamp = int(timestamp_raw)
    except ValueError:
        return _json_error("Invalid timestamp", status=401)

    now = int(time.time())
    if abs(now - timestamp) > max_skew_seconds:
        return _json_error("Request expired", status=401)

    payload = _get_request_payload(request)
    if payload is None:
        return _json_error("Invalid JSON body")

    qq_number = str(payload.get("qq_number", "")).strip()
    if not qq_number:
        return _json_error("qq_number is required")

    if not _is_valid_signature(token, timestamp_raw, qq_number, signature, secret):
        logger.warning("QQMonitor API authentication failed: invalid signature.")
        return _json_error("Invalid token or signature", status=401)

    entry = (
        QqMonitorEntry.objects.select_related("submitted_by")
        .filter(qq_number=qq_number)
        .order_by("-updated_at")
        .first()
    )
    if not entry:
        logger.info("QQMonitor API queried qq_number=%s: not found", qq_number)
        return JsonResponse(
            {
                "ok": True,
                "qq_number": qq_number,
                "exists": False,
                "in_alliance": False,
                "main_account_id": None,
                "nickname": None,
            }
        )

    user = entry.submitted_by
    in_alliance = False
    alliance_id = None
    if user:
        member_alliance_ids = _get_member_alliance_ids()
        in_alliance, alliance_id = _is_user_in_current_alliance(user, member_alliance_ids)

    logger.info(
        "QQMonitor API queried qq_number=%s: exists=%s, in_alliance=%s",
        qq_number,
        True,
        in_alliance,
    )
    return JsonResponse(
        {
            "ok": True,
            "qq_number": qq_number,
            "exists": True,
            "in_alliance": in_alliance,
            "main_account_id": entry.main_character_id,
            "nickname": entry.nickname,
            "main_character_id": entry.main_character_id,
            "submitted_by_user_id": user.id if user else None,
            "current_alliance_id": alliance_id,
        }
    )
