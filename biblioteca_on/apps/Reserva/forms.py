from django import forms
from .models import *
from django.core.exceptions import ValidationError


class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        libro = cleaned_data.get('libro')
        reserva_id = self.instance.pk  # ID de la reserva (si es edición, ya tendrá valor)

        if libro and libro.ejemplares <= 0:
            raise ValidationError(f"No hay Ejemplares disponibles para el libro {libro.titulo}.")

        # Verificamos si existe alguna reserva activa para ese usuario **que no sea la actual**
        if Reservacion.objects.filter(usuario=usuario, estado_reservacion__in=['Reservado', 'No Completa']).exclude(
                id=reserva_id).exists():
            raise ValidationError('El usuario ya tiene una reservación vigente.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar libros con ejemplares disponibles
        self.fields['libro'].queryset = Libro.objects.filter(ejemplares__gt=0, condicion=Libro.Condicion.DISPONIBLE)

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'


