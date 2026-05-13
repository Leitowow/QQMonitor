from django.db import migrations, models


def deduplicate_qq_number(apps, schema_editor):
    """
    Keep one row per qq_number before applying unique constraint.

    If duplicates exist, keep the latest updated row.
    """

    QqMonitorEntry = apps.get_model("qqmonitor", "QqMonitorEntry")
    duplicates = (
        QqMonitorEntry.objects.values("qq_number")
        .annotate(row_count=models.Count("id"))
        .filter(row_count__gt=1)
    )

    for item in duplicates:
        rows = QqMonitorEntry.objects.filter(qq_number=item["qq_number"]).order_by(
            "-updated_at", "-id"
        )
        survivor = rows.first()
        if survivor is None:
            continue
        rows.exclude(id=survivor.id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("qqmonitor", "0003_one_entry_per_user"),
    ]

    operations = [
        migrations.RunPython(deduplicate_qq_number, migrations.RunPython.noop),
        migrations.RemoveConstraint(
            model_name="qqmonitorentry",
            name="uq_qqmonitor_qq_and_main_character",
        ),
        migrations.RemoveField(
            model_name="qqmonitorentry",
            name="main_character_id",
        ),
        migrations.AddConstraint(
            model_name="qqmonitorentry",
            constraint=models.UniqueConstraint(
                fields=("qq_number",),
                name="uq_qqmonitor_qq_number",
            ),
        ),
    ]
