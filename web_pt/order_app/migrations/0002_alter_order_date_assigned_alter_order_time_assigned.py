# Generated by Django 5.0.3 on 2024-03-13 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_assigned',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha a realizar'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_assigned',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora a realizar'),
        ),
    ]
