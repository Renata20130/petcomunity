# Generated by Django 5.2.3 on 2025-07-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_profile_ciudad_alter_profile_region"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="nombre_farmacia",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
