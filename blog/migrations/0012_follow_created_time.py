# Generated by Django 5.1.2 on 2025-01-28 12:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0011_alter_postvideo_file_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="follow",
            name="created_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
