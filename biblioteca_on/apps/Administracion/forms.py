from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),  # Inicialmente vacío, luego filtrado
        widget=forms.SelectMultiple,  # Usar un select múltiple
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener los modelos registrados en el Admin
        registered_models = [
            model for model in self.get_admin_models()  # Obtener modelos registrados en el Admin
        ]

        # Obtener los permisos asociados a esos modelos
        content_types = ContentType.objects.filter(model__in=[model._meta.model_name for model in registered_models])

        # Filtrar los permisos de acuerdo a los ContentTypes obtenidos
        permisos_modelos = Permission.objects.filter(content_type__in=content_types)

        # Establecer la queryset de permisos
        self.fields['permissions'].queryset = permisos_modelos

    def get_admin_models(self):
        # Obtener los modelos registrados en el admin
        # Esto depende de los modelos y apps que tengas registrados en tu admin
        from django.contrib import admin
        registered_models = []
        for model_admin in admin.site._registry.values():
            registered_models.append(model_admin.model)
        return registered_models
