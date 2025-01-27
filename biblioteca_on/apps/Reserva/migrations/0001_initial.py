# Generated by Django 5.1.5 on 2025-01-26 06:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Libro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_reservacion', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de reservación')),
                ('fecha_limite_reservacion', models.DateField(blank=True, null=True, verbose_name='Fecha límite de reservación')),
                ('estado_reservacion', models.CharField(choices=[('Reservado', 'Reservado'), ('Vencido', 'Vencido'), ('No Completa', 'No Completa'), ('Completa', 'Completa'), ('Anulada', 'Anulada')], default='Reservado', max_length=20, verbose_name='Estado de la reservación')),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libro.libro', verbose_name='Libro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Reservación',
                'verbose_name_plural': 'Reservaciones',
            },
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_recoleccion', models.DateField(blank=True, null=True, verbose_name='Fecha de recolección')),
                ('fecha_devolucion', models.DateField(blank=True, null=True, verbose_name='Fecha de devolución')),
                ('fecha_limite_devolucion', models.DateField(blank=True, null=True, verbose_name='Fecha límite de devolución')),
                ('estado_prestamo', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('RECOGIDO', 'Recogido'), ('DEVUELTO', 'Devuelto')], default='PENDIENTE', max_length=20, verbose_name='Estado de la prestamo')),
                ('recargo_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Recargo Total')),
                ('estado', models.BooleanField(default=False, verbose_name='Estado del prestamo')),
                ('reservacion', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='Reserva.reservacion', verbose_name='Reservación')),
            ],
            options={
                'verbose_name': 'Préstamo',
                'verbose_name_plural': 'Préstamos',
            },
        ),
    ]
