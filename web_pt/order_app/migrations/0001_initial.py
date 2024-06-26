# Generated by Django 5.0.4 on 2024-04-07 18:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('contract_number', models.IntegerField(primary_key=True, serialize=False, verbose_name='Nro. De Contrato')),
                ('customer_name', models.CharField(max_length=50, verbose_name='Nombre Cliente')),
                ('email', models.CharField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone_1', models.CharField(max_length=20, verbose_name='Teléfono 1')),
                ('phone_2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono 2')),
                ('address', models.CharField(max_length=300, verbose_name='Dirección')),
                ('customer_type', models.CharField(choices=[('FR', 'Fibra Residencial'), ('FP', 'Fibra PYME'), ('OT', 'Otro')], default='FR', max_length=2, verbose_name='Tipo De Cliente')),
                ('category', models.CharField(choices=[('INS', 'Instalación'), ('MIG', 'Migración'), ('MUD', 'Mudanza'), ('M&M', 'Migración y mudanza'), ('SER', 'Servicio'), ('OTR', 'Otro')], default='INS', max_length=3, verbose_name='Categoría')),
                ('plan', models.CharField(choices=[('BA', 'Básico'), ('BP', 'Básico Plus'), ('BR', 'Bronce'), ('PL', 'Plata'), ('OR', 'Oro'), ('EM', 'Emprendedor'), ('PR', 'Productivo'), ('PP', 'Productivo Pro'), ('VP', 'Visionario Pro'), ('SD', 'Sin definir')], default='BR', max_length=2, verbose_name='Plan')),
                ('assigned_company', models.CharField(blank=True, max_length=100, null=True, verbose_name='Asignado a')),
                ('seller', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vendedor')),
                ('comment', models.CharField(blank=True, max_length=300, null=True, verbose_name='Observaciones')),
                ('date_received', models.DateField(blank=True, null=True, verbose_name='Fecha Recibida')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha De Creación')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Última Modificación')),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Onu',
            fields=[
                ('serial', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='Serial')),
            ],
            options={
                'verbose_name': 'onu',
                'verbose_name_plural': 'onus',
            },
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, verbose_name='Código')),
                ('document_id', models.IntegerField(verbose_name='Nro. De Cédula')),
                ('phone_1', models.CharField(max_length=20, verbose_name='Teléfono 1')),
                ('phone_2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono 2')),
                ('address', models.CharField(max_length=200, verbose_name='Dirección')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'technician',
                'verbose_name_plural': 'technicians',
            },
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('serial', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='Serial')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_app.technician', verbose_name='Técnico')),
            ],
            options={
                'verbose_name': 'router',
                'verbose_name_plural': 'routers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateField(blank=True, null=True, verbose_name='Fecha a realizar')),
                ('time_assigned', models.TimeField(blank=True, null=True, verbose_name='Hora a realizar')),
                ('completed', models.BooleanField(default=False, verbose_name='Completada')),
                ('zone', models.IntegerField(blank=True, null=True, verbose_name='Zona')),
                ('olt', models.IntegerField(blank=True, null=True, verbose_name='OLT')),
                ('pon', models.IntegerField(blank=True, null=True, verbose_name='PON')),
                ('card', models.IntegerField(blank=True, null=True, verbose_name='Tarjeta')),
                ('box', models.IntegerField(blank=True, null=True, verbose_name='Caja')),
                ('port', models.IntegerField(blank=True, null=True, verbose_name='Puerto')),
                ('box_power', models.FloatField(blank=True, null=True, verbose_name='Potencia Caja')),
                ('house_power', models.FloatField(blank=True, null=True, verbose_name='Potencia Roseta')),
                ('drop_serial', models.IntegerField(blank=True, null=True, verbose_name='Serial DROP')),
                ('drop_used', models.IntegerField(blank=True, null=True, verbose_name='DROP')),
                ('hook_used', models.IntegerField(blank=True, default=0, null=True, verbose_name='Tensores')),
                ('fast_conn_used', models.IntegerField(blank=True, default=2, null=True, verbose_name='Conectores')),
                ('customer_confirmation', models.IntegerField(choices=[(0, 'No citado'), (1, 'Pendiente'), (2, 'Confirmado')], default=0, verbose_name='Confirmación Cliente')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha De Creación')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Última Modificación')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order_app.customer', verbose_name='Cliente')),
                ('onu', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_app.onu', verbose_name='Onu')),
                ('router', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_app.router', verbose_name='Router')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', related_query_name='order', to='order_app.technician', verbose_name='Técnico')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.AddField(
            model_name='onu',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_app.technician', verbose_name='Técnico'),
        ),
    ]
