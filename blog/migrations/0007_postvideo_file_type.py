# Generated by Django 5.1.2 on 2025-01-27 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_post_saved"),
    ]

    operations = [
        migrations.AddField(
            model_name="postvideo",
            name="file_type",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
