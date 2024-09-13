# Generated by Django 5.1 on 2024-09-13 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contenidos', '0008_alter_contenidos_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='descripcion',
            field=models.TextField(null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]