from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from .forms import *
from .models import Usuario
from ..Libro.models import Libro
from django.contrib.auth.decorators import login_not_required

# Create your views here.

@method_decorator(login_not_required, name='dispatch')
class HomePageView(ListView):
    model = Libro
    template_name = 'home.html'
    context_object_name = 'libros'

    def get_queryset(self):
        # Obtener solo los libros ordenados por el número de recomendaciones (de mayor a menor)
        return Libro.objects.filter(recomendaciones__gt=0).order_by('-recomendaciones')

@method_decorator(login_not_required, name='dispatch')
class RegistrationView(CreateView):
    model = Usuario
    form_class = RegistroUsuarioLectorForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('Login:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "¡Te has registrado correctamente! Ahora puedes iniciar sesión.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al intentar registrarte. Por favor, revisa los campos.")
        return super().form_invalid(form)