from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from django.contrib.auth.models import Group
import random
import string


class CrearUsuario(UserCreationForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Seleccione un grupo",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Grupo"
    )

    class Meta:
        model = Usuario
        fields = [
            'dni',
            'first_name',
            'last_name',
            'username',
            'email',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'foto_perfil',
            'condicion',
            'saldo',
            'estado',
            'group',
            'password1',  # El campo password1 ya está gestionado por el formulario UserCreationForm
            'password2',  # El campo password2 también se incluye automáticamente
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'condicion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'dni': 'DNI',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'foto_perfil': 'Foto de Perfil',
            'condicion': 'Condición',
            'saldo': 'Saldo',
            'estado': 'Estado',
            'group': 'Grupo',
        }


    def save(self, commit=True):
        usuario = super().save(commit=False)

        if commit:
            usuario.save()  # Guardamos el usuario para obtener el id

        # Asignamos el grupo solo si ha sido seleccionado
        group = self.cleaned_data.get('group')
        if group:
            usuario.groups.add(group)  # Usamos add para agregar el grupo

        return usuario

class EditarUsuario(UserChangeForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Seleccione un grupo",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Grupo"
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'dni',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'foto_perfil',
            'condicion',
            'saldo',
            'estado',
            'group',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'condicion': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'dni': 'DNI',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'foto_perfil': 'Foto de Perfil',
            'condicion': 'Condición',
            'saldo': 'Saldo',
            'estado': 'Estado',
            'group': 'Grupo',
        }

    def save(self, commit=True):
        # Guarda el usuario con el nuevo grupo
        usuario = super().save(commit=False)
        group = self.cleaned_data.get('group')
        if commit:
            usuario.save()
            if group:
                usuario.groups.clear()  # Elimina todos los grupos actuales
                usuario.groups.add(group)  # Añade solo el grupo seleccionado
        return usuario



class RegistroUsuarioLectorForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'dni', 'first_name', 'last_name',
            'email', 'telefono', 'direccion',
            'fecha_nacimiento', 'username', 'password1', 'password2', 'foto_perfil'
        ]
        widgets = {
            'dni': forms.TextInput(attrs={'maxlength': '10', 'pattern': '^\d{10}$', 'title': 'El DNI debe contener 10 dígitos'}),
            'telefono': forms.TextInput(attrs={'maxlength': '10', 'pattern': '^\d{10}$', 'title': 'El teléfono debe contener 10 dígitos'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'required': 'required'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña', 'required': 'required'})
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(dni) != 10 or not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener exactamente 10 dígitos.")
        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) != 10 or not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener exactamente 10 dígitos y ser numérico.")
        return telefono

    def save(self, commit=True):
        usuario = super().save(commit=False)

        # Guardar primero al usuario para asignarle un ID
        if commit:
            usuario.save()

        # Asignar siempre el grupo Lector
        lector_rol = Group.objects.get(id=3)
        usuario.groups.add(lector_rol)

        # Asegurarse de que otras condiciones se establezcan
        usuario.condicion = 'Habilitado'
        usuario.estado = True

        # Guardar los cambios del usuario
        if commit:
            usuario.save()

        return usuario
