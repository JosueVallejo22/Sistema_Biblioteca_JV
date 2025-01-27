from django.urls import path
from apps.Reserva.views import *

app_name = 'Reservacion'
urlpatterns = [
    path('reservaciones/', ReservacionListView.as_view(), name='reservaciones'),
    path('reservaciones/create', ReservacionCreateView.as_view(), name='reservaciones_create'),
    path('reservaciones/reservar/<int:pk>/', RealizarReservaView.as_view(), name='reservaciones_reserva'),
    path('reservaciones/update/<pk>', ReservacionUpdateView.as_view(), name='reservaciones_update'),
    path('reservaciones/delete/<pk>', ReservacionDeleteView.as_view(), name='reservaciones_delete'),

    path('prestamo/list/', PrestamoListView.as_view(), name='prestamo_list'),
    path('prestamo/detail/<pk>', PrestamoDetailView.as_view(), name='prestamo_detail'),
    path('prestamo/update/<pk>', PrestamoUpdateView.as_view(), name='prestamo_update'),

]