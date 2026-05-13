from django.db import migrations, models


def deduplicate_user_entries(apps, schema_editor):
    """
    Keep one row per submitted_by before applying unique constraint.

    For users with multiple records, keep the latest updated row.
    """

    QqMonitorEntry = apps.get_model("qqmonitor", "QqMonitorEntry")
    duplicates = (
        QqMonitorEntry.objects.exclude(submitted_by__isnull=True)
        .values("submitted_by")
        .annotate(row_count=models.Count("id"))
        .filter(row_count__gt=1)
    )

    for item in duplicates:
        rows = QqMonitorEntry.objects.filter(submitted_by=item["submitted_by"]).order_by(
            "-updated_at", "-id"
        )
        survivor = rows.first()
        if survivor is None:
            continue
        rows.exclude(id=survivor.id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("qqmonitor", "0002_unique_qq_main_character"),
    ]

    operations = [
        migrations.RunPython(deduplicate_user_entries, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="qqmonitorentry",
            constraint=models.UniqueConstraint(
                fields=("submitted_by",),
                name="uq_qqmonitor_submitted_by_user",
            ),
        ),
    ]
