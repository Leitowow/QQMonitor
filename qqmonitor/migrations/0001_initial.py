from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="QqMonitorEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("qq_number", models.CharField(max_length=32, verbose_name="QQ号")),
                ("main_character_id", models.BigIntegerField(verbose_name="主角色ID")),
                ("nickname", models.CharField(max_length=64, verbose_name="昵称")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "submitted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="qqmonitor_entries",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="提交用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "QQ监控记录",
                "verbose_name_plural": "QQ监控记录",
                "ordering": ["-created_at"],
            },
        ),
    ]
