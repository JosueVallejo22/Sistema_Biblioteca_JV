from datetime import timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from apps.Reserva.forms import *
from apps.Reserva.models import *
from django.utils import timezone
from django.views import View

class ReservacionListView(PermissionRequiredMixin, ListView):
    model = Reservacion
    context_object_name = 'reservaciones'
    template_name = 'reservacion/reservaciones_list.html'
    ordering = ['-id']
    permission_required = 'Reserva.view_reservacion'


class ReservacionCreateView(PermissionRequiredMixin, CreateView):
    model = Reservacion
    form_class = ReservacionForm
    template_name = 'reservacion/reservacion_form.html'
    success_url = reverse_lazy('Reservacion:reservaciones')
    permission_required = 'Reserva.create_reservacion'


    def form_valid(self, form):
        # Obtener el libro de la reservación
        libro = form.cleaned_data['libro']

        # Si la fecha limite no es proporcionada, se calcula automáticamente
        if not form.cleaned_data['fecha_limite_reservacion']:
            form.instance.fecha_limite_reservacion = form.instance.fecha_reservacion + timedelta(days=3)

        # Modificar ejemplares en función del estado de la reservación
        if form.instance.estado_reservacion in ['Reservado', 'No Completa']:
            # Resta 1 ejemplar cuando está en estado 'Reservado' o 'No Completa'
            libro.ejemplares -= 1
            libro.save()

        with transaction.atomic():
            reservacion = form.save()
            prestamo = Prestamo.objects.create(
                reservacion=reservacion,
                recargo_total= 0,
                estado_prestamo = Prestamo.Estado_Prestamo.PENDIENTE,
                estado = False
            )

        return super().form_valid(form)



class ReservacionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Reservacion
    form_class = ReservacionForm
    template_name = 'reservacion/reservacion_form.html'
    success_url = reverse_lazy('Reservacion:reservaciones')
    permission_required = 'Reserva.update_reservacion'

    def form_valid(self, form):
        # Obtener el libro de la reservación
        libro = form.cleaned_data['libro']

        # Si la fecha limite no es proporcionada, se calcula automáticamente
        if not form.cleaned_data['fecha_limite_reservacion']:
            form.instance.fecha_limite_reservacion = form.instance.fecha_reservacion + timedelta(days=3)

        # Si la reservación fue previamente completada o vencida, restauramos los ejemplares
        if form.instance.pk:
            old_reservacion = Reservacion.objects.get(pk=form.instance.pk)
            if old_reservacion.estado_reservacion in ['Reservado', 'No Completa']:
                libro.ejemplares += 1  # Cuando se deshace una reserva, se vuelve a aumentar ejemplares
                libro.save()

        # Modificar ejemplares dependiendo de la nueva condición
        if form.instance.estado_reservacion in ['Reservado', 'No Completa']:
            # Resta 1 ejemplar cuando está en estado 'Reservado' o 'No Completa'
            libro.ejemplares -= 1
            libro.save()


        return super().form_valid(form)
class ReservacionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reservacion
    template_name = 'reservacion/reservacion_confirm_delete.html'
    success_url = reverse_lazy('Reservacion:reservaciones')
    permission_required = 'Reserva.delete_reservacion'


######### PRESTAMOS

class PrestamoListView(PermissionRequiredMixin, ListView):
    model = Prestamo
    context_object_name = 'prestamos'
    paginate_by = 10
    template_name = 'reservacion/prestamo_list.html'
    ordering = ['-id']
    permission_required = 'Reserva.view_prestamo'

class PrestamoDetailView(PermissionRequiredMixin, DetailView):
    model = Prestamo
    context_object_name = 'prestamo'
    template_name = 'reservacion/prestamo_detail.html'
    permission_required = 'Reserva.view_prestamo'

from django.http import HttpResponse

class PrestamoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'reservacion/prestamo_form.html'
    permission_required = 'Reserva.update_prestamo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestamo'] = self.get_object()  # Envía el objeto préstamo al template
        return context

    def get_success_url(self):
        return reverse('Reservacion:prestamo_detail', kwargs={'pk': self.object.pk})


#################################################################################################


class RealizarReservaView(PermissionRequiredMixin, View):
    permission_required = 'Reserva.add_reservacion'

    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return render(request, 'bibliotecario/libro/libro_detail.html', {'libro': libro})

    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)

        # Validación 1: Verificar si el libro tiene ejemplares disponibles
        if libro.ejemplares <= 0:
            messages.error(request, f"No hay ejemplares disponibles para el libro {libro.titulo}.")
            return redirect('Libros:libros_detail', pk=libro.pk)

        # Validación 2: Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Debes estar autenticado para hacer una reserva.")
            return redirect('Login:login')

        # Validación 3: Verificar si el usuario ya tiene una reserva activa
        reserva_activa = Reservacion.objects.filter(
            usuario=request.user,
            estado_reservacion__in=['Reservado', 'No Completa']
        ).exists()
        if reserva_activa:
            messages.error(request, "Ya tienes una reservación activa. No puedes realizar otra hasta completarla.")
            return redirect('Libros:libros_detail', pk=libro.pk)

        # Validación 4: Verificar si el saldo pendiente del usuario es mayor a 5
        saldo_usuario = request.user.saldo  # Asume que 'saldo' es un campo decimal en el modelo de Usuario
        if saldo_usuario > 5:
            messages.error(request, "No puedes realizar una reserva mientras tengas un saldo pendiente superior a $5.00 .")
            return redirect('Libros:libros_detail', pk=libro.pk)

        # Crear la reserva automáticamente
        nueva_reservacion = Reservacion(
            usuario=request.user,
            libro=libro,
            fecha_reservacion=timezone.now(),
            estado_reservacion='Reservado',
            fecha_limite_reservacion=timezone.now() + timedelta(days=3)  # Fecha límite de 3 días
        )

        # Guardar la reserva
        nueva_reservacion.save()

        # Restar un ejemplar del libro
        libro.ejemplares -= 1
        libro.save()

        # Crear un préstamo pendiente
        Prestamo.objects.create(
            reservacion=nueva_reservacion,
            recargo_total=0,
            estado_prestamo=Prestamo.Estado_Prestamo.PENDIENTE,
            estado=False
        )

        messages.success(request, f"¡Reserva realizada con éxito para el libro {libro.titulo}!")
        return redirect('Libros:libros_detail', pk=libro.pk)
