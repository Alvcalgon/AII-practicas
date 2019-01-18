# Generated by Django 2.0 on 2019-01-18 14:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ADSL_FIBRA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('velocidad', models.CharField(max_length=30)),
                ('fijo', models.CharField(max_length=40)),
                ('promociones', models.CharField(max_length=75)),
                ('coste_mensual', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('tipo', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^Fibra|ADSL$', 'Fibra o ADSL. Ningun otro valor valido')])),
            ],
        ),
        migrations.CreateModel(
            name='Operadora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('enlace_web', models.URLField(validators=[django.core.validators.URLValidator()])),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('velocidad', models.CharField(max_length=30)),
                ('fijo', models.CharField(max_length=40)),
                ('movil', models.CharField(max_length=30)),
                ('tv', models.CharField(max_length=50)),
                ('promociones', models.CharField(max_length=75)),
                ('coste_mensual', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('operadora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Operadora')),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa_movil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('minutos', models.CharField(max_length=50)),
                ('internet_movil', models.CharField(max_length=30)),
                ('promociones', models.CharField(max_length=75)),
                ('coste_mensual', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('tipo', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^Contrato|Tarjeta$', 'Una tarifa de movil es de Contrato o por Tarjeta ')])),
                ('operadora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Operadora')),
            ],
        ),
        migrations.AddField(
            model_name='adsl_fibra',
            name='operadora',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Operadora'),
        ),
    ]