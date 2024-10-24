# Generated by Django 5.1.1 on 2024-10-04 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contenidos', '0008_alter_contenidos_options'),
        ('TableroKanban', '0002_remove_columna_tablerokanb_orden_97fa3a_idx_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarjeta',
            name='estado',
        ),
        migrations.AddField(
            model_name='columna',
            name='estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Contenidos.estado'),
            preserve_default=False,
        ),
    ]