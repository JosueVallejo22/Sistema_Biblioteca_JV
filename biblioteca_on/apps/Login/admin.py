from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
# Register your models here.

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'dni', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']  # Personaliza los campos a mostrar
    search_fields = ['username', 'email', 'dni']  # Puedes personalizar qué campos permitir para búsqueda


admin.site.register(Usuario, UsuarioAdmin)

