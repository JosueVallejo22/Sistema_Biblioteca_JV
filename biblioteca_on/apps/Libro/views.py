from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import *
# Create your views here.

#### CATEGORIA ####
class CategoriaView(PermissionRequiredMixin, ListView):
    model = Categoria
    context_object_name = 'categorias'
    ordering = ['categoria']
    template_name = 'bibliotecario/categoria/categoria_list.html'
    permission_required = 'Libro.view_categorias'

class CategoriaCreateView(PermissionRequiredMixin, CreateView):
    model = Categoria
    form_class = CrearCategoria
    template_name = 'bibliotecario/categoria/categoria_form.html'
    success_url = reverse_lazy('Libros:categorias')
    permission_required = 'Libro.add_categoria'


class CategoriaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Categoria
    form_class = CrearCategoria
    template_name = 'bibliotecario/categoria/categoria_form.html'
    success_url = reverse_lazy('Libros:categorias')
    permission_required = 'Libro.change_categoria'

class CategoriaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'bibliotecario/categoria/categoria_confirm_delete.html'
    success_url = reverse_lazy('Libros:categorias')
    permission_required = 'Libro.delete_categoria'

#### AUTOR ####
class AutorView(PermissionRequiredMixin, ListView):
    model = Autor
    context_object_name = 'autors'
    ordering = ['nombre']
    template_name = 'bibliotecario/autor/autor_list.html'
    permission_required = 'Libro.view_autor'

class AutorCreateView(PermissionRequiredMixin, CreateView):
    model = Autor
    form_class = CrearAutor
    template_name = 'bibliotecario/autor/autor_form.html'
    success_url = reverse_lazy('Libros:autors')
    permission_required = 'Libro.add_autor'

class AutorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Autor
    form_class = CrearAutor
    template_name = 'bibliotecario/autor/autor_form.html'
    success_url = reverse_lazy('Libros:autors')
    permission_required = 'Libro.change_autor'

class AutorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Autor
    template_name = 'bibliotecario/autor/autor_confirm_delete.html'
    success_url = reverse_lazy('Libros:autors')
    permission_required = 'Libro.delete_autor'

#### LIBROS ####

class LibroView(PermissionRequiredMixin, ListView):
    model = Libro
    context_object_name = 'libros'
    ordering = ['titulo']
    template_name = 'bibliotecario/libro/libro_list.html'
    permission_required = 'Libro.view_libro'

class LibroDetailView(PermissionRequiredMixin, DetailView):
    model = Libro
    context_object_name = 'libro'
    template_name = 'bibliotecario/libro/libro_detail.html'
    permission_required = 'Libro.view_libro'
class RecomendarLibroView(PermissionRequiredMixin, View):
    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)

        if not libro.recomendacion_set.filter(usuario = request.user).exists():
            Recomendacion.objects.create(libro=libro, usuario = request.user)

            libro.recomendaciones += 1
            libro.save()

        return redirect('Libros:libros_detail', pk=libro.id)
    permission_required = 'Libro.add_recomendacion'

class LibroCreateView(PermissionRequiredMixin, CreateView):
    model = Libro
    form_class = CrearLibro
    template_name = 'bibliotecario/libro/libro_form.html'
    success_url = reverse_lazy('Libros:libros')
    permission_required = 'Libro.add_libro'

class LibroUpdateView(PermissionRequiredMixin, UpdateView):
    model = Libro
    form_class = CrearLibro
    template_name = 'bibliotecario/libro/libro_form.html'
    success_url = reverse_lazy('Libros:libros')
    permission_required = 'Libro.change_libro'

class LibroDeleteView(PermissionRequiredMixin, DeleteView):
    model = Libro
    template_name = 'bibliotecario/libro/libro_confirm_delete.html'
    success_url = reverse_lazy('Libros:libros')
    permission_required = 'Libro.delete_libro'