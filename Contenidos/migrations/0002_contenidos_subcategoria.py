# Generated by Django 5.1 on 2024-09-20 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Categoria', '0002_initial'),
        ('Contenidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenidos',
            name='subcategoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Categoria.subcategoria'),
        ),
    ]
