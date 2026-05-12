"""URL routes for QQMonitor."""

from django.urls import path

from qqmonitor import views

app_name = "qqmonitor"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/v1/verify-qq/", views.api_verify_qq, name="api_verify_qq"),
]
