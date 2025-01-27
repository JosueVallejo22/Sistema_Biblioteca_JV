from datetime import timedelta

from django.db import models
from apps.Libro.models import Libro
from apps.Login.models import Usuario
from django.utils import timezone

class Reservacion(models.Model):
    class Estado_Reservacion(models.TextChoices):
        RESERVADO = 'Reservado', 'Reservado'
        VENCIDO = 'Vencido', 'Vencido'
        NO_COMPLETA = 'No Completa', 'No Completa'
        COMPLETA = 'Completa', 'Completa'
        ANULADA = 'Anulada', 'Anulada'

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, verbose_name="Libro")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha_reservacion = models.DateField(default=timezone.now, verbose_name="Fecha de reservación")
    fecha_limite_reservacion = models.DateField(null=True, blank=True, verbose_name="Fecha límite de reservación")
    estado_reservacion = models.CharField(max_length=20, choices=Estado_Reservacion.choices, default=Estado_Reservacion.RESERVADO, verbose_name="Estado de la reservación")

    def actualizar_estado(self, nuevo_estado, ajustar_ejemplares=True):
        """Actualiza el estado y ajusta los ejemplares del libro según el cambio."""
        libro = self.libro

        if ajustar_ejemplares:
            # Cambios por transición de estado
            if self.estado_reservacion in ['Reservado', 'No Completa']:
                libro.ejemplares += 1  # Revertir si fue reservado
            if nuevo_estado in ['Reservado', 'No Completa']:
                libro.ejemplares -= 1  # Restar si ahora es reservado o recogido

        self.estado_reservacion = nuevo_estado
        self.save()
        libro.save()


    class Meta:
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"

    def __str__(self):
        return f'Reservación de libro {self.libro.titulo} a nombre de {self.usuario.first_name} {self.usuario.last_name}'




##### PRESTAMO #####
class Prestamo(models.Model):
    class Estado_Prestamo(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente',
        RECOGIDO = 'RECOGIDO', 'Recogido',
        DEVUELTO = 'DEVUELTO', 'Devuelto'
    reservacion = models.OneToOneField(Reservacion, on_delete=models.PROTECT, verbose_name='Reservación')  # Cada préstamo depende de una reserva
    fecha_recoleccion = models.DateField(null=True, blank=True, verbose_name="Fecha de recolección")
    fecha_devolucion = models.DateField(null=True, blank=True, verbose_name="Fecha de devolución")
    fecha_limite_devolucion = models.DateField(null=True, blank=True, verbose_name="Fecha límite de devolución")
    estado_prestamo = models.CharField(max_length=20, choices=Estado_Prestamo.choices, default=Estado_Prestamo.PENDIENTE, verbose_name="Estado de la prestamo")
    recargo_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Recargo Total")
    estado = models.BooleanField(default=False, verbose_name="Estado del prestamo")

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"

    def save(self, *args, **kwargs):
        # Lógica de validación para fecha de recolección
        if self.fecha_recoleccion and self.estado_prestamo == self.Estado_Prestamo.PENDIENTE:
            self.estado_prestamo = self.Estado_Prestamo.RECOGIDO
            self.fecha_limite_devolucion = self.fecha_recoleccion + timedelta(days=7)

        # Lógica de validación para fecha de devolución
        if self.fecha_devolucion:
            # Calcular atraso si devuelve después de la fecha límite
            if self.fecha_limite_devolucion and self.fecha_devolucion > self.fecha_limite_devolucion:
                dias_atraso = (self.fecha_devolucion - self.fecha_limite_devolucion).days
                self.recargo_total = dias_atraso * 3  # $3 por cada día de atraso
            self.estado_prestamo = self.Estado_Prestamo.DEVUELTO

        if self.estado_prestamo == self.Estado_Prestamo.DEVUELTO:
            # Si se devuelve el libro, sumar el recargo al saldo del usuario
            usuario = self.reservacion.usuario
            usuario.saldo += self.recargo_total  # Sumar el recargo al saldo del usuario
            usuario.save()

        if self.estado_prestamo == 'PENDIENTE':
            self.reservacion.actualizar_estado('Reservado', ajustar_ejemplares=False)
        elif self.estado_prestamo == 'RECOGIDO':
            self.reservacion.actualizar_estado('No Completa', ajustar_ejemplares=False)
        elif self.estado_prestamo == 'DEVUELTO':
            self.reservacion.actualizar_estado('Completa', ajustar_ejemplares=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Préstamo del libro {self.reservacion.libro.titulo} para {self.reservacion.usuario.first_name} {self.reservacion.usuario.last_name}'


