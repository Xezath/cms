from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias', views.categorias, name='categorias'),
    path('categorias/crear', views.crear, name='crear'),
    path('categorias/editar', views.editar, name='editar')
]