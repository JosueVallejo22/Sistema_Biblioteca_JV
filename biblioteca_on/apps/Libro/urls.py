from django.urls import path
from apps.Libro.views import *

app_name = 'Libros'
urlpatterns = [
    ########### CATEGORIAS
    path('categorias/', CategoriaView.as_view(), name='categorias' ),
    path('categorias/create/', CategoriaCreateView.as_view(), name='categorias_create' ),
    path('categorias/update/<pk>/', CategoriaUpdateView.as_view(), name='categorias_update' ),
    path('categorias/delete/<pk>/', CategoriaDeleteView.as_view(), name='categorias_delete' ),

    ########### AUTORES
    path('autors/', AutorView.as_view(), name='autors' ),
    path('autors/create/', AutorCreateView.as_view(), name='autors_create'),
    path('autors/update/<pk>/', AutorUpdateView.as_view(), name='autors_update'),
    path('autors/delete/<pk>/', AutorDeleteView.as_view(), name='autors_delete'),

    ########### LIBROS
    path('libros/', LibroView.as_view(), name='libros' ),
    path('libros/create/', LibroCreateView.as_view(), name='libros_create'),
    path('libros/update/<pk>/', LibroUpdateView.as_view(), name='libros_update'),
    path('libros/delete/<pk>/', LibroDeleteView.as_view(), name='libros_delete'),
    path('libros/detail/<pk>/', LibroDetailView.as_view(), name='libros_detail'),
    path('libros/<int:libro_id>/recomendar/', RecomendarLibroView.as_view(), name='recomendar_libro'),


]