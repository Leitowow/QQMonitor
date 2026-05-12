"""URL routes for QQMonitor."""

from django.urls import path

from qqmonitor import views

app_name = "qqmonitor"

urlpatterns = [
    path("", views.index, name="index"),
]
