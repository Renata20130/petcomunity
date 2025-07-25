# Generated by Django 5.2.3 on 2025-07-18 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "adopciones",
            "0015_mascotaabandonada_ciudad_mascotaabandonada_especie_and_more",
        ),
        ("ubicacion", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mascotaabandonada",
            name="ciudad",
            field=models.ForeignKey(
                to="ubicacion.ciudad",
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                
            ),
        ),
        migrations.AlterField(
            model_name="mascotaabandonada",
            name="region",
            field=models.ForeignKey(
                to='ubicacion.Region',
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                
            ),
        ),
    ]
