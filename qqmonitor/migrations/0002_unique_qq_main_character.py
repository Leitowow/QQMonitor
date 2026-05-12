from django.db import migrations, models


def deduplicate_entries(apps, schema_editor):
    """
    Idempotent data cleanup before adding unique constraint.

    If old data already contains duplicates for (qq_number, main_character_id),
    keep the oldest row and delete the rest.
    """

    QqMonitorEntry = apps.get_model("qqmonitor", "QqMonitorEntry")
    duplicates = (
        QqMonitorEntry.objects.values("qq_number", "main_character_id")
        .annotate(row_count=models.Count("id"))
        .filter(row_count__gt=1)
    )
    for item in duplicates:
        rows = (
            QqMonitorEntry.objects.filter(
                qq_number=item["qq_number"],
                main_character_id=item["main_character_id"],
            )
            .order_by("created_at", "id")
        )
        survivor = rows.first()
        if survivor is None:
            continue
        rows.exclude(id=survivor.id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("qqmonitor", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(deduplicate_entries, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="qqmonitorentry",
            constraint=models.UniqueConstraint(
                fields=("qq_number", "main_character_id"),
                name="uq_qqmonitor_qq_and_main_character",
            ),
        ),
    ]
