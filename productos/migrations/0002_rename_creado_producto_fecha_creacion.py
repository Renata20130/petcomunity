# Generated by Django 5.2.3 on 2025-07-03 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("productos", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="producto",
            old_name="creado",
            new_name="fecha_creacion",
        ),
    ]
