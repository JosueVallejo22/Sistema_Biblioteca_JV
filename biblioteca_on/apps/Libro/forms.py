from django import forms
from .models import *

class CrearCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class CrearAutor(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'

class CrearLibro(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
