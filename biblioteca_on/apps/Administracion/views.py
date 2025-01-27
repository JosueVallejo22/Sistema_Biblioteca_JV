from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from apps.Administracion.forms import GroupForm
from apps.Login.forms import CrearUsuario, EditarUsuario
from apps.Login.models import Usuario


# Create your views here.
# CRUD PARA LOS GRUPOS (ROLES)
class GroupListView(PermissionRequiredMixin, ListView):
    model = Group
    template_name = 'administracion/group_list.html'
    context_object_name = 'groups'
    ordering = ['id']
    permission_required = 'auth.view_group'

class GroupDetailView(PermissionRequiredMixin, DetailView):
    model = Group
    template_name = 'administracion/group_detail.html'
    context_object_name = 'group'
    permission_required = 'auth.view_group'


class GroupCreateView(PermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'administracion/group_form.html'
    success_url = reverse_lazy('Administracion:group_list')
    permission_required = 'auth.add_group'


class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'administracion/group_form.html'
    success_url = reverse_lazy('Administracion:group_list')
    permission_required = 'auth.change_group'


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = Group
    template_name = 'administracion/group_confirm_delete.html'
    success_url = reverse_lazy('Administracion:group_list')
    permission_required = 'auth.delete_group'






#CRUD PARA LOS USUARIOS
class UsuarioListView(PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = 'administracion/usuarios_list.html'
    context_object_name = 'usuarios'
    ordering = ['username']
    permission_required = 'Login.view_usuario'


class UsuarioCreateView(PermissionRequiredMixin, CreateView):
    model = Usuario
    form_class = CrearUsuario
    template_name = 'administracion/usuarios_form.html'
    success_url = reverse_lazy('Administracion:usuario_list')
    permission_required = 'Login.add_usuario'

    def form_invalid(self, form):
        # Muestra los errores del formulario en la consola para depuración
        print("Errores del formulario:", form.errors)
        return super().form_invalid(form)

class UsuarioUpdateView(PermissionRequiredMixin, UpdateView):
    model = Usuario
    form_class = EditarUsuario
    template_name = 'administracion/usuarios_form.html'
    success_url = reverse_lazy('Administracion:usuario_list')
    permission_required = 'Login.change_usuario'

class UsuarioDeleteView(PermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'administracion/usuarios_confirm_delete.html'
    success_url = reverse_lazy('Administracion:usuario_list')
    permission_required = 'Login.delete_usuario'