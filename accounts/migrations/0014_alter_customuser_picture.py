# Generated by Django 5.1.2 on 2025-02-03 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_remove_customuser_password2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="picture",
            field=models.FileField(blank=True, upload_to="images/profile"),
        ),
    ]
