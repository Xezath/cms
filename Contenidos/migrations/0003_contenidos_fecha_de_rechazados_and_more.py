# Generated by Django 5.1 on 2024-11-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contenidos', '0002_contenidos_numero_lecturas'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenidos',
            name='fecha_de_rechazados',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contenidos',
            name='fecha_publicacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
