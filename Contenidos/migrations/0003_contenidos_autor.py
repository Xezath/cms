# Generated by Django 5.1 on 2024-09-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contenidos', '0002_contenidos_contenido_contenidos_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenidos',
            name='autor',
            field=models.CharField(default='unknown', max_length=100),
        ),
    ]