# Generated by Django 5.1.1 on 2024-10-06 14:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TableroKanban', '0004_remove_tablero_usuario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tarjeta',
            options={'permissions': [('visualiza su contenido', 'Puede ver solo su propio contenido')]},
        ),
        migrations.AddField(
            model_name='tarjeta',
            name='autor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
