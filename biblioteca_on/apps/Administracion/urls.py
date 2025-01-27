from django.urls import path
from apps.Administracion.views import *

app_name = 'Administracion'
urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create', GroupCreateView.as_view(), name='group_create'),
    path('groups/detail/<pk>', GroupDetailView.as_view(), name='group_detail'),
    path('groups/edit/<pk>', GroupUpdateView.as_view(), name='group_update'),
    path('groups/delete/<pk>', GroupDeleteView.as_view(), name='group_delete'),

    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/create', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/edit/<pk>', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/delete/<pk>', UsuarioDeleteView.as_view(), name='usuario_delete'),
]