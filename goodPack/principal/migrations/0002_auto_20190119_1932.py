# Generated by Django 2.0 on 2019-01-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete',
            name='fijo',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='movil',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='nombre',
            field=models.CharField(max_length=75),
        ),
    ]